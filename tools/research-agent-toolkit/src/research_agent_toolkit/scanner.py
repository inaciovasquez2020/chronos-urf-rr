from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

LEAN_DECL = re.compile(r"^\s*(?:theorem|lemma|def|structure|class|inductive|abbrev)\s+([A-Za-z0-9_'.]+)", re.M)
LEAN_IMPORT = re.compile(r"^\s*import\s+([A-Za-z0-9_'.]+)", re.M)
SHELL_SOURCE = re.compile(r"^\s*(?:source|\.)\s+['\"]?([^'\"\s]+)", re.M)


@dataclass
class Node:
    path: str
    language: str
    symbols: list[str] = field(default_factory=list)


@dataclass
class Edge:
    source: str
    target: str
    kind: str


@dataclass
class Graph:
    root: str
    nodes: list[Node]
    edges: list[Edge]

    def to_dict(self) -> dict:
        return {
            "root": self.root,
            "nodes": [asdict(x) for x in self.nodes],
            "edges": [asdict(x) for x in self.edges],
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n")


def _language(path: Path) -> str:
    return {
        ".py": "python",
        ".lean": "lean",
        ".sh": "shell",
        ".json": "json",
        ".md": "markdown",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
    }.get(path.suffix.lower(), "other")


def _python_symbols_and_imports(text: str) -> tuple[list[str], list[str]]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [], []
    symbols: list[str] = []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return sorted(set(symbols)), sorted(set(imports))


def _literal_file_refs(text: str, known: set[str]) -> list[str]:
    refs = []
    for candidate in known:
        if candidate and candidate in text:
            refs.append(candidate)
    return refs


def scan(root: str | Path, include_suffixes: Iterable[str] | None = None) -> Graph:
    root = Path(root).resolve()
    suffixes = set(include_suffixes or [".py", ".lean", ".sh", ".json", ".md", ".toml", ".yaml", ".yml"])
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in suffixes and ".git" not in p.parts)
    rels = [p.relative_to(root).as_posix() for p in files]
    known = set(rels)
    nodes: list[Node] = []
    edges: list[Edge] = []

    module_to_path: dict[str, str] = {}
    for rel in rels:
        if rel.endswith(".py"):
            module = rel[:-3].replace("/", ".")
            if module.endswith(".__init__"):
                module = module[:-9]
            module_to_path[module] = rel
        elif rel.endswith(".lean"):
            module_to_path[rel[:-5].replace("/", ".")] = rel

    for path, rel in zip(files, rels):
        text = path.read_text(errors="replace")
        lang = _language(path)
        symbols: list[str] = []
        imports: list[str] = []
        if lang == "python":
            symbols, imports = _python_symbols_and_imports(text)
        elif lang == "lean":
            symbols = sorted(set(LEAN_DECL.findall(text)))
            imports = sorted(set(LEAN_IMPORT.findall(text)))
        elif lang == "shell":
            for target in SHELL_SOURCE.findall(text):
                t = (path.parent / target).resolve()
                try:
                    target_rel = t.relative_to(root).as_posix()
                except ValueError:
                    continue
                if target_rel in known:
                    edges.append(Edge(rel, target_rel, "source"))

        nodes.append(Node(rel, lang, symbols))
        for imp in imports:
            target = module_to_path.get(imp)
            if target:
                edges.append(Edge(rel, target, "import"))
        for target in _literal_file_refs(text, known):
            if target != rel:
                edges.append(Edge(rel, target, "literal_ref"))

    dedup = {(e.source, e.target, e.kind): e for e in edges}
    return Graph(str(root), nodes, sorted(dedup.values(), key=lambda e: (e.source, e.target, e.kind)))


def reverse_closure(graph: Graph, changed: Iterable[str]) -> list[str]:
    """Return files that may depend on changed paths, including the changed files."""
    reverse: dict[str, set[str]] = {}
    for edge in graph.edges:
        reverse.setdefault(edge.target, set()).add(edge.source)
    seen = set(changed)
    stack = list(changed)
    while stack:
        item = stack.pop()
        for dep in reverse.get(item, ()):
            if dep not in seen:
                seen.add(dep)
                stack.append(dep)
    return sorted(seen)
