#!/usr/bin/env python3

from __future__ import annotations

from collections import deque, defaultdict
from typing import Dict, Set, Tuple
from canonical_label import canonical_ball_code_iso

Vertex = int
Graph = Dict[Vertex, Set[Vertex]]

def add_edge(G: Graph, u: Vertex, v: Vertex) -> None:
    G.setdefault(u, set()).add(v)
    G.setdefault(v, set()).add(u)

def num_edges(G: Graph) -> int:
    return sum(len(nbrs) for nbrs in G.values()) // 2

def cycle_rank(G: Graph) -> int:
    visited: Set[Vertex] = set()
    components = 0
    for v in G:
        if v in visited:
            continue
        components += 1
        stack = [v]
        visited.add(v)
        while stack:
            x = stack.pop()
            for y in G[x]:
                if y not in visited:
                    visited.add(y)
                    stack.append(y)
    return num_edges(G) - len(G) + components

def type_set(G: Graph, R: int) -> Set[int]:
    return {canonical_ball_code_iso(G, v, R) for v in G}

def transition_set(G: Graph, R: int) -> Set[Tuple[int, int]]:
    T: Set[Tuple[int, int]] = set()
    for u in G:
        cu = canonical_ball_code_iso(G, u, R)
        for v in G[u]:
            cv = canonical_ball_code_iso(G, v, R)
            T.add((cu, cv))
    return T

def connected_regular_base(d: int) -> Graph:
    if d == 2:
        n = 6
        G: Graph = {i: set() for i in range(n)}
        for i in range(n):
            add_edge(G, i, (i + 1) % n)
        return G
    if d == 3:
        n = 8
        G = {i: set() for i in range(n)}
        edges = [
            (0,1),(1,3),(3,2),(2,0),
            (4,5),(5,7),(7,6),(6,4),
            (0,4),(1,5),(2,6),(3,7),
        ]
        for u,v in edges:
            add_edge(G,u,v)
        return G
    raise ValueError

def main():
    G = connected_regular_base(3)
    print("type_count:", len(type_set(G, 2)))
    print("cycle_rank:", cycle_rank(G))

if __name__ == "__main__":
    main()
