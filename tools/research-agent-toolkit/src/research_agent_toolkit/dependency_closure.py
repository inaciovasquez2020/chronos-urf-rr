from __future__ import annotations

from .provenance import ProvenanceGraph, forward_closure
from .scanner import Graph, reverse_closure


def combined_closure(file_graph: Graph, provenance: ProvenanceGraph, seeds: list[str]) -> list[str]:
    known_files = {node.path for node in file_graph.nodes}
    seen = set(seeds)
    while True:
        before = set(seen)
        file_seeds = [item for item in seen if item in known_files]
        seen.update(reverse_closure(file_graph, file_seeds))
        seen.update(forward_closure(provenance, list(seen)))
        if seen == before:
            return sorted(seen)
