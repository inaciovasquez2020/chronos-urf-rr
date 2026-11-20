"""Bounded structural analysis, not factual verification."""

import json
from pathlib import Path

from .adaptive_radius import RadiusAuditor, IncompleteAudit


def audit_graph(graph, max_radius=8, max_work=5_000_000):
    if type(max_radius) is not int or max_radius < 0:
        raise ValueError("Invalid radius")

    if type(max_work) is not int or not 0 < max_work <= 5_000_000:
        raise ValueError("Invalid work limit")

    if not isinstance(graph, dict):
        raise ValueError("Expected graph object")

    nodes = graph.get("nodes")
    edges = graph.get("edges")

    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("Expected nodes and edges arrays")

    if len(nodes) > 256 or len(edges) > 8192:
        raise IncompleteAudit("Graph size guard")

    names = set()

    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("Invalid node")

        name = node.get("path")

        if not isinstance(name, str) or not name or len(name) > 4096:
            raise ValueError("Invalid node path")

        if name in names:
            raise ValueError("Duplicate node")

        names.add(name)

    directed = set()
    kinds = set()

    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("Invalid edge")

        a = edge.get("source")
        b = edge.get("target")
        kind = edge.get("kind")

        if not all(isinstance(x, str) for x in (a, b, kind)):
            raise ValueError("Invalid edge fields")

        if a not in names or b not in names:
            raise ValueError("Unknown endpoint")

        directed.add((a, b))
        kinds.add(kind)

    undirected = {
        tuple(sorted((a, b)))
        for a, b in directed
        if a != b
    }

    engine = RadiusAuditor(
        names,
        undirected,
        max_vertices=256,
        max_edges=4096,
        max_work=max_work,
    )

    adj = {v: set() for v in names}

    for a, b in directed:
        engine.tick()
        adj[a].add(b)

    # Directed semantics are audited separately.
    reach = {}

    for root in sorted(names):
        seen = set()
        stack = list(adj[root])

        while stack:
            engine.tick()
            v = stack.pop()

            if v in seen:
                continue

            seen.add(v)

            for target in adj[v]:
                engine.tick()

                if target not in seen:
                    stack.append(target)

        reach[root] = seen

    remaining = set(names)
    cyclic = []

    while remaining:
        root = min(remaining)
        component = set()

        for v in remaining:
            engine.tick()

            if v == root or (
                v in reach[root] and root in reach[v]
            ):
                component.add(v)

        remaining -= component

        if len(component) > 1 or root in adj[root]:
            cyclic.append(sorted(component))

    profile = engine.adaptive(max_radius)

    return {
        "status": "COMPLETE",
        "field": "GF(2)",
        "vertices": len(names),
        "directed_edges": len(directed),
        "undirected_edges": len(undirected),
        "edge_kinds": sorted(kinds),
        "directed_cyclic_components": cyclic,
        "profile": profile,
        "work_units": engine.work,
        "factual_accuracy": "NOT_MEASURED",
        "reasoning_improvement": "NOT_MEASURED",
        "dependency_completeness": "NOT_ESTABLISHED",
        "mutation_authorized": False,
    }


def audit_file(path, max_radius=8, max_work=5_000_000):
    with Path(path).open("rb") as stream:
        raw = stream.read(2_000_001)

    if len(raw) > 2_000_000:
        raise IncompleteAudit("JSON input size guard")

    return audit_graph(
        json.loads(raw),
        max_radius=max_radius,
        max_work=max_work,
    )
