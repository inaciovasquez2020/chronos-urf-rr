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


def build_provenance(
    root: str | Path,
    manifest: dict,
    lean_graph: LeanExactGraph | None = None,
) -> ProvenanceGraph:
    root = Path(root).resolve()
    declared = (
        {d.name for d in lean_graph.declarations}
        if lean_graph is not None
        else set()
    )

    nodes: dict[tuple[str, str], ProvenanceNode] = {}
    edges: dict[tuple[str, str, str], ProvenanceEdge] = {}

    chains = manifest.get("chains", [])
    if not isinstance(chains, list):
        raise ValueError(
            "provenance manifest 'chains' must be a list"
        )

    for idx, chain in enumerate(chains):
        if not isinstance(chain, dict):
            raise ValueError(
                f"provenance chain {idx} must be an object"
            )

        roots = [
            kind
            for kind in ("theorem", "claim")
            if chain.get(kind)
        ]

        if len(roots) != 1:
            raise ValueError(
                f"provenance chain {idx} must contain exactly "
                "one of theorem or claim"
            )

        required = ["generator", "artifact", "test"]
        missing = [
            key
            for key in required
            if not chain.get(key)
        ]

        if missing:
            raise ValueError(
                f"provenance chain {idx} missing: "
                + ", ".join(missing)
            )

        root_kind = roots[0]
        root_id = str(chain[root_kind])
        generator = str(chain["generator"])
        artifact = str(chain["artifact"])
        test = str(chain["test"])

        if root_kind == "theorem":
            if lean_graph is None:
                raise ValueError(
                    "theorem provenance requires an exact Lean graph"
                )

            if root_id not in declared:
                raise ValueError(
                    "provenance theorem is not in exact Lean graph: "
                    + root_id
                )

        for role, rel in (
            ("generator", generator),
            ("artifact", artifact),
            ("test", test),
        ):
            path = (root / rel).resolve()

            try:
                path.relative_to(root)
            except ValueError as exc:
                raise ValueError(
                    f"{role} escapes repository root: {rel}"
                ) from exc

            if not path.is_file():
                raise FileNotFoundError(
                    f"missing provenance {role}: {rel}"
                )

        for kind, value in (
            (root_kind, root_id),
            ("generator", generator),
            ("artifact", artifact),
            ("test", test),
        ):
            nodes[(kind, value)] = ProvenanceNode(
                value,
                kind,
            )

        for source, target, kind in (
            (
                root_id,
                generator,
                f"{root_kind}_to_generator",
            ),
            (
                generator,
                artifact,
                "generator_to_artifact",
            ),
            (
                artifact,
                test,
                "artifact_to_test",
            ),
        ):
            edges[(source, target, kind)] = ProvenanceEdge(
                source,
                target,
                kind,
            )

    return ProvenanceGraph(
        sorted(
            nodes.values(),
            key=lambda x: (x.kind, x.id),
        ),
        sorted(
            edges.values(),
            key=lambda x: (
                x.source,
                x.target,
                x.kind,
            ),
        ),
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
