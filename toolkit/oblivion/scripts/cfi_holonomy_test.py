#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple

Vertex = str
Edge = Tuple[int, int]
Graph = Dict[Vertex, Set[Vertex]]


def ordered_edge(e: Edge) -> Edge:
    a, b = e
    return (a, b) if a <= b else (b, a)


def edge_name(e: Edge) -> str:
    a, b = ordered_edge(e)
    return f"e{a}_{b}"


def add_edge(G: Graph, u: Vertex, v: Vertex) -> None:
    G.setdefault(u, set()).add(v)
    G.setdefault(v, set()).add(u)


def make_base_cycle(n: int) -> List[Edge]:
    return [ordered_edge((i, (i + 1) % n)) for i in range(n)]


def incident_edges(base_edges: List[Edge], v: int) -> List[Edge]:
    return [e for e in base_edges if v in e]


@dataclass(frozen=True)
class CFIData:
    graph: Graph
    base_edges: Tuple[Edge, ...]
    twisted_edges: Tuple[Edge, ...]
    edge_transport_bit: Dict[Edge, int]
    left_ports: Dict[Edge, Tuple[Vertex, Vertex]]
    right_ports: Dict[Edge, Tuple[Vertex, Vertex]]


def cfi_labeled_pair_on_cycle(n: int, twisted_edges: Iterable[Edge]) -> Tuple[CFIData, CFIData]:
    base_edges = tuple(make_base_cycle(n))
    twisted = {ordered_edge(e) for e in twisted_edges}

    G0: Graph = defaultdict(set)
    G1: Graph = defaultdict(set)

    left_ports_0: Dict[Edge, Tuple[Vertex, Vertex]] = {}
    right_ports_0: Dict[Edge, Tuple[Vertex, Vertex]] = {}
    left_ports_1: Dict[Edge, Tuple[Vertex, Vertex]] = {}
    right_ports_1: Dict[Edge, Tuple[Vertex, Vertex]] = {}

    for e in base_edges:
        en = edge_name(e)
        l0 = f"{en}:L0"
        l1 = f"{en}:L1"
        r0 = f"{en}:R0"
        r1 = f"{en}:R1"
        G0[l0]; G0[l1]; G0[r0]; G0[r1]
        G1[l0]; G1[l1]; G1[r0]; G1[r1]
        left_ports_0[e] = (l0, l1)
        right_ports_0[e] = (r0, r1)
        left_ports_1[e] = (l0, l1)
        right_ports_1[e] = (r0, r1)

    for v in range(n):
        inc = [edge_name(e) for e in incident_edges(list(base_edges), v)]
        deg = len(inc)
        for mask in range(1 << deg):
            if bin(mask).count("1") % 2 != 0:
                continue
            bits = tuple((mask >> i) & 1 for i in range(deg))
            label = "".join(str(b) for b in bits)
            gv = f"v{v}:P{label}"
            G0[gv]
            G1[gv]
            for i, en in enumerate(inc):
                b = bits[i]
                add_edge(G0, gv, f"{en}:L{b}")
                add_edge(G1, gv, f"{en}:L{b}")

    transport0: Dict[Edge, int] = {}
    transport1: Dict[Edge, int] = {}

    for e in base_edges:
        en = edge_name(e)
        l0, l1 = f"{en}:L0", f"{en}:L1"
        r0, r1 = f"{en}:R0", f"{en}:R1"

        add_edge(G0, l0, r0)
        add_edge(G0, l1, r1)
        transport0[e] = 0

        if e in twisted:
            add_edge(G1, l0, r1)
            add_edge(G1, l1, r0)
            transport1[e] = 1
        else:
            add_edge(G1, l0, r0)
            add_edge(G1, l1, r1)
            transport1[e] = 0

    D0 = CFIData(
        graph=dict(G0),
        base_edges=base_edges,
        twisted_edges=tuple(sorted(set())),
        edge_transport_bit=transport0,
        left_ports=left_ports_0,
        right_ports=right_ports_0,
    )
    D1 = CFIData(
        graph=dict(G1),
        base_edges=base_edges,
        twisted_edges=tuple(sorted(twisted)),
        edge_transport_bit=transport1,
        left_ports=left_ports_1,
        right_ports=right_ports_1,
    )
    return D0, D1


def fundamental_cycle_edges(base_edges: Tuple[Edge, ...], n: int) -> List[Edge]:
    want = [ordered_edge((i, (i + 1) % n)) for i in range(n)]
    have = set(base_edges)
    return [e for e in want if e in have]


def holonomy_phi(data: CFIData, n: int) -> int:
    cyc = fundamental_cycle_edges(data.base_edges, n)
    x = 0
    for e in cyc:
        x ^= data.edge_transport_bit[e]
    return x


def num_edges(G: Graph) -> int:
    return sum(len(G[v]) for v in G) // 2


def cycle_rank(G: Graph) -> int:
    seen: Set[Vertex] = set()
    comps = 0
    for s in G:
        if s in seen:
            continue
        comps += 1
        q = [s]
        seen.add(s)
        while q:
            x = q.pop()
            for y in G[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
    return num_edges(G) - len(G) + comps


def run() -> None:
    n = 6
    D0, D1 = cfi_labeled_pair_on_cycle(n, {(0, 1)})

    print("phi(G0) =", holonomy_phi(D0, n))
    print("phi(G1) =", holonomy_phi(D1, n))
    print("cycle_rank(G0) =", cycle_rank(D0.graph))
    print("cycle_rank(G1) =", cycle_rank(D1.graph))
    print("twisted_edges_G1 =", list(D1.twisted_edges))


if __name__ == "__main__":
    run()
