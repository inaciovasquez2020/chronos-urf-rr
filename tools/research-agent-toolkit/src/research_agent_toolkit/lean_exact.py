from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class LeanDeclaration:
    name: str
    module: str
    kind: str


@dataclass(frozen=True)
class LeanDependency:
    source: str
    target: str


@dataclass
class LeanExactGraph:
    modules: list[str]
    declarations: list[LeanDeclaration]
    edges: list[LeanDependency]

    def to_dict(self) -> dict:
        return {
            "modules": self.modules,
            "declarations": [asdict(x) for x in self.declarations],
            "edges": [asdict(x) for x in self.edges],
        }


def _lean_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_probe(modules: list[str]) -> str:
    if not modules:
        raise ValueError("at least one Lean module is required")
    imports = "\n".join(f"import {module}" for module in modules)
    targets = ", ".join(_lean_string(module) for module in modules)
    return f'''import Lean
{imports}

open Lean Elab Command

private def ratTargets : List String := [{targets}]

private partial def ratConsts : Expr → List Name
  | .const n _ => [n]
  | .app f a => ratConsts f ++ ratConsts a
  | .lam _ t b _ => ratConsts t ++ ratConsts b
  | .forallE _ t b _ => ratConsts t ++ ratConsts b
  | .letE _ t v b _ => ratConsts t ++ ratConsts v ++ ratConsts b
  | .mdata _ e => ratConsts e
  | .proj n _ e => n :: ratConsts e
  | _ => []

elab "#rat_exact_deps" : command => do
  let env ← getEnv
  for (name, info) in env.constants do
    match Lean.Server.getModuleContainingDecl? env name with
    | none => pure ()
    | some moduleName =>
      if ratTargets.contains moduleName.toString then
        let kind := reprStr (ConstantKind.ofConstantInfo info)
        liftIO <| IO.println s!"RAT_DECL\\t{{moduleName}}\\t{{kind}}\\t{{name}}"
        let bodyRefs := match info.value? true with
          | some value => ratConsts value
          | none => []
        let refs := (ratConsts info.type ++ bodyRefs).eraseDups
        for dep in refs do
          if dep != name then
            liftIO <| IO.println s!"RAT_EDGE\\t{{name}}\\t{{dep}}"

#rat_exact_deps
'''


def parse_probe_output(stdout: str, modules: list[str]) -> LeanExactGraph:
    declarations: list[LeanDeclaration] = []
    edges: list[LeanDependency] = []
    for raw in stdout.splitlines():
        if raw.startswith("RAT_DECL\t"):
            parts = raw.split("\t", 3)
            if len(parts) != 4:
                raise ValueError(f"malformed Lean declaration record: {raw!r}")
            _, module, kind, name = parts
            declarations.append(LeanDeclaration(name=name, module=module, kind=kind))
        elif raw.startswith("RAT_EDGE\t"):
            parts = raw.split("\t", 2)
            if len(parts) != 3:
                raise ValueError(f"malformed Lean dependency record: {raw!r}")
            _, source, target = parts
            edges.append(LeanDependency(source=source, target=target))
    declarations = sorted(set(declarations), key=lambda x: (x.module, x.name, x.kind))
    edges = sorted(set(edges), key=lambda x: (x.source, x.target))
    return LeanExactGraph(list(modules), declarations, edges)


def exact_lean_dependencies(
    root: str | Path,
    modules: list[str],
    *,
    lake: str = "lake",
    timeout: int = 120,
) -> LeanExactGraph:
    root = Path(root).resolve()
    if not ((root / "lakefile.lean").exists() or (root / "lakefile.toml").exists()):
        raise FileNotFoundError(f"no lakefile.lean or lakefile.toml under {root}")
    probe = build_probe(modules)
    with tempfile.NamedTemporaryFile("w", suffix=".lean", prefix="rat_exact_", dir=root, delete=False) as fh:
        fh.write(probe)
        probe_path = Path(fh.name)
    try:
        proc = subprocess.run(
            [lake, "env", "lean", str(probe_path)],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    finally:
        probe_path.unlink(missing_ok=True)
    if proc.returncode != 0:
        first = next((line for line in proc.stderr.splitlines() if line.strip()), "Lean dependency probe failed")
        raise RuntimeError(first)
    return parse_probe_output(proc.stdout, modules)


def reverse_declaration_closure(graph: LeanExactGraph, changed: list[str]) -> list[str]:
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
