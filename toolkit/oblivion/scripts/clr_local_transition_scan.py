#!/usr/bin/env python3

from __future__ import annotations

from collections import deque, defaultdict
from dataclasses import dataclass
from itertools import combinations
import hashlib
import json
import random
from typing import Dict, Iterable, List, Set, Tuple

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
        q = [v]
        visited.add(v)
        while q:
            x = q.pop()
            for y in G[x]:
                if y not in visited:
                    visited.add(y)
                    q.append(y)
    return num_edges(G) - len(G) + components


def bfs_ball(G: Graph, root: Vertex, R: int) -> Set[Vertex]:
    seen = {root}
    q = deque([(root, 0)])
    while q:
        x, d = q.popleft()
        if d == R:
            continue
        for y in G[x]:
            if y not in seen:
                seen.add(y)
                q.append((y, d + 1))
    return seen


def induced_subgraph(G: Graph, verts: Set[Vertex]) -> Graph:
    H: Graph = {}
    for v in verts:
        H[v] = {u for u in G[v] if u in verts}
    return H


def canonical_ball_code(G: Graph, root: Vertex, R: int) -> str:
    ball = bfs_ball(G, root, R)
    H = induced_subgraph(G, ball)
    dist: Dict[Vertex, int] = {root: 0}
    q = deque([root])
    while q:
        x = q.popleft()
        for y in H[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    ordered = sorted(H.keys(), key=lambda v: (dist[v], len(H[v]), v))
    idx = {v: i for i, v in enumerate(ordered)}
    edge_list = []
    for u in ordered:
        for v in H[u]:
            if idx[u] < idx[v]:
                edge_list.append((idx[u], idx[v]))
    payload = {
        "root": idx[root],
        "dist": [dist[v] for v in ordered],
        "deg": [len(H[v]) for v in ordered],
        "edges": edge_list,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def type_set(G: Graph, R: int) -> Set[str]:
    return {canonical_ball_code(G, v, R) for v in G}


def transition_set(G: Graph, R: int) -> Set[Tuple[str, str]]:
    T: Set[Tuple[str, str]] = set()
    for u in G:
        cu = canonical_ball_code(G, u, R)
        for v in G[u]:
            cv = canonical_ball_code(G, v, R)
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
        cube_edges = [
            (0, 1), (1, 3), (3, 2), (2, 0),
            (4, 5), (5, 7), (7, 6), (6, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]
        for u, v in cube_edges:
            add_edge(G, u, v)
        return G
    raise ValueError("supported degrees: d in {2,3}")


def random_n_lift(base: Graph, n: int, seed: int) -> Graph:
    rng = random.Random(seed)
    Vb = sorted(base.keys())
    oriented = []
    used = set()
    for u in Vb:
        for v in base[u]:
            if (v, u) not in used:
                oriented.append((u, v))
                used.add((u, v))
    G: Graph = {}
    for u in Vb:
        for i in range(n):
            G[(u * n) + i] = set()
    for u, v in oriented:
        perm = list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            a = (u * n) + i
            b = (v * n) + perm[i]
            add_edge(G, a, b)
    return G


def homogeneous(G: Graph, R: int) -> bool:
    return len(type_set(G, R)) == 1


def adjacency_automaton_from_samples(samples: Iterable[Graph], R: int) -> Tuple[Set[str], Set[Tuple[str, str]]]:
    P: Set[str] = set()
    F: Set[Tuple[str, str]] = set()
    for G in samples:
        P |= type_set(G, R)
        F |= transition_set(G, R)
    return P, F


def summarize_counterexample_search(R: int, d: int, lift_sizes: List[int], trials: int) -> Dict[str, object]:
    base = connected_regular_base(d)
    samples = [base]
    witnesses = []
    for n in lift_sizes:
        for t in range(trials):
            G = random_n_lift(base, n=n, seed=1000 * n + t)
            samples.append(G)
            witnesses.append(
                {
                    "n": n,
                    "trial": t,
                    "homogeneous": homogeneous(G, R),
                    "cycle_rank": cycle_rank(G),
                    "num_vertices": len(G),
                    "num_edges": num_edges(G),
                    "num_types": len(type_set(G, R)),
                }
            )
    P, F = adjacency_automaton_from_samples(samples, R)
    homogeneous_hits = [w for w in witnesses if w["homogeneous"]]
    max_rank_hom = max((w["cycle_rank"] for w in homogeneous_hits), default=None)
    return {
        "R": R,
        "degree_bound": d,
        "base_num_vertices": len(base),
        "base_cycle_rank": cycle_rank(base),
        "type_count": len(P),
        "transition_count": len(F),
        "homogeneous_witnesses": homogeneous_hits,
        "max_cycle_rank_among_homogeneous_witnesses": max_rank_hom,
        "all_trials": witnesses,
    }


def main() -> None:
    R = 2
    d = 3
    lift_sizes = [4, 8, 12, 16]
    trials = 8
    out = summarize_counterexample_search(R=R, d=d, lift_sizes=lift_sizes, trials=trials)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
