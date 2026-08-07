from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .lean_exact import LeanExactGraph


@dataclass(frozen=True)
class ProvenanceNode:
    id: str
    kind: str


@dataclass(frozen=True)
class ProvenanceEdge:
    source: str
    target: str
    kind: str


@dataclass
class ProvenanceGraph:
    nodes: list[ProvenanceNode]
    edges: list[ProvenanceEdge]

    def to_dict(self) -> dict:
        return {
            "nodes": [asdict(x) for x in self.nodes],
            "edges": [asdict(x) for x in self.edges],
        }


def load_manifest(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def build_provenance(root: str | Path, manifest: dict, lean_graph: LeanExactGraph) -> ProvenanceGraph:
    root = Path(root).resolve()
    declared = {d.name for d in lean_graph.declarations}
    nodes: dict[tuple[str, str], ProvenanceNode] = {}
    edges: dict[tuple[str, str, str], ProvenanceEdge] = {}

    chains = manifest.get("chains", [])
    if not isinstance(chains, list):
        raise ValueError("provenance manifest 'chains' must be a list")

    for idx, chain in enumerate(chains):
        if not isinstance(chain, dict):
            raise ValueError(f"provenance chain {idx} must be an object")
        required = ["theorem", "generator", "artifact", "test"]
        missing = [key for key in required if not chain.get(key)]
        if missing:
            raise ValueError(f"provenance chain {idx} missing: {', '.join(missing)}")

        theorem = str(chain["theorem"])
        generator = str(chain["generator"])
        artifact = str(chain["artifact"])
        test = str(chain["test"])

        if theorem not in declared:
            raise ValueError(f"provenance theorem is not in exact Lean graph: {theorem}")
        for role, rel in (("generator", generator), ("artifact", artifact), ("test", test)):
            path = (root / rel).resolve()
            try:
                path.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"{role} escapes repository root: {rel}") from exc
            if not path.is_file():
                raise FileNotFoundError(f"missing provenance {role}: {rel}")

        for kind, value in (
            ("theorem", theorem),
            ("generator", generator),
            ("artifact", artifact),
            ("test", test),
        ):
            nodes[(kind, value)] = ProvenanceNode(value, kind)
        for source, target, kind in (
            (theorem, generator, "theorem_to_generator"),
            (generator, artifact, "generator_to_artifact"),
            (artifact, test, "artifact_to_test"),
        ):
            edges[(source, target, kind)] = ProvenanceEdge(source, target, kind)

    return ProvenanceGraph(
        sorted(nodes.values(), key=lambda x: (x.kind, x.id)),
        sorted(edges.values(), key=lambda x: (x.source, x.target, x.kind)),
    )


def forward_closure(graph: ProvenanceGraph, changed: list[str]) -> list[str]:
    forward: dict[str, set[str]] = {}
    for edge in graph.edges:
        forward.setdefault(edge.source, set()).add(edge.target)
    seen = set(changed)
    stack = list(changed)
    while stack:
        item = stack.pop()
        for dep in forward.get(item, ()):
            if dep not in seen:
                seen.add(dep)
                stack.append(dep)
    return sorted(seen)
