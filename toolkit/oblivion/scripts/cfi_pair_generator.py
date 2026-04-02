#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

Vertex = str
Graph = Dict[Vertex, Set[Vertex]]
Edge = Tuple[int, int]


def add_edge(G: Graph, u: Vertex, v: Vertex) -> None:
    G.setdefault(u, set()).add(v)
    G.setdefault(v, set()).add(u)


def make_base_cycle(n: int) -> List[Edge]:
    return [(i, (i + 1) % n) for i in range(n)]


def incident_edges(base_edges: List[Edge], v: int) -> List[Edge]:
    out: List[Edge] = []
    for e in base_edges:
        if v in e:
            out.append(e)
    return out


def ordered_edge(e: Edge) -> Edge:
    a, b = e
    return (a, b) if a <= b else (b, a)


def edge_name(e: Edge) -> str:
    a, b = ordered_edge(e)
    return f"e{a}_{b}"


def cfi_pair_on_cycle(n: int, twisted_edges: Iterable[Edge]) -> Tuple[Graph, Graph]:
    base_edges = [ordered_edge(e) for e in make_base_cycle(n)]
    twisted = {ordered_edge(e) for e in twisted_edges}

    G0: Graph = defaultdict(set)
    G1: Graph = defaultdict(set)

    # edge gadgets: two endpoint copies per base edge
    for e in base_edges:
        en = edge_name(e)
        for bit in (0, 1):
            G0[f"{en}:L{bit}"]
            G0[f"{en}:R{bit}"]
            G1[f"{en}:L{bit}"]
            G1[f"{en}:R{bit}"]

    # vertex gadgets: parity-even assignments on incident edges
    for v in range(n):
        inc = [edge_name(e) for e in incident_edges(base_edges, v)]
        deg = len(inc)
        for mask in range(1 << deg):
            parity = bin(mask).count("1") % 2
            if parity != 0:
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

    # connect the two sides of each edge gadget
    for e in base_edges:
        en = edge_name(e)
        if e in twisted:
            add_edge(G0, f"{en}:L0", f"{en}:R0")
            add_edge(G0, f"{en}:L1", f"{en}:R1")
            add_edge(G1, f"{en}:L0", f"{en}:R1")
            add_edge(G1, f"{en}:L1", f"{en}:R0")
        else:
            add_edge(G0, f"{en}:L0", f"{en}:R0")
            add_edge(G0, f"{en}:L1", f"{en}:R1")
            add_edge(G1, f"{en}:L0", f"{en}:R0")
            add_edge(G1, f"{en}:L1", f"{en}:R1")

    return dict(G0), dict(G1)


def num_edges(G: Graph) -> int:
    return sum(len(G[v]) for v in G) // 2


def cycle_rank(G: Graph) -> int:
    seen: Set[Vertex] = set()
    comps = 0
    for s in G:
        if s in seen:
            continue
        comps += 1
        stack = [s]
        seen.add(s)
        while stack:
            x = stack.pop()
            for y in G[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
    return num_edges(G) - len(G) + comps


def main() -> None:
    base_n = 6
    twist = {(0, 1)}
    G0, G1 = cfi_pair_on_cycle(base_n, twist)
    print("G0_vertices", len(G0))
    print("G1_vertices", len(G1))
    print("G0_edges", num_edges(G0))
    print("G1_edges", num_edges(G1))
    print("G0_cycle_rank", cycle_rank(G0))
    print("G1_cycle_rank", cycle_rank(G1))


if __name__ == "__main__":
    main()


def cfi_labeled_pair_on_cycle(base_n: int, twist: set):
    G0, G1 = {}, {}
    for v in range(base_n):
        for g in [G0, G1]:
            for bit in range(2):
                g[(v, bit)] = {}
    used = set()
    for v in range(base_n):
        u = (v + 1) % base_n
        key = (min(v, u), max(v, u))
        if key in used:
            continue
        used.add(key)
        for bit in range(2):
            G0[(v, bit)][(u, bit)] = 0
            G0[(u, bit)][(v, bit)] = 0
            is_twisted = (v, u) in twist or (u, v) in twist
            flip = 1 if is_twisted else 0
            G1[(v, bit)][(u, bit ^ flip)] = flip
            G1[(u, bit ^ flip)][(v, bit)] = flip
    return G0, G1
