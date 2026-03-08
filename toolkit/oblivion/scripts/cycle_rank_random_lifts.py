#!/usr/bin/env python3
import argparse
import json
from collections import deque

import networkx as nx
import numpy as np


def random_lift_k4(p: int, seed: int) -> nx.Graph:
    rng = np.random.default_rng(seed)
    base_vertices = [0, 1, 2, 3]
    base_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    perms = {}
    for e in base_edges:
        perms[e] = rng.permutation(p)

    G = nx.Graph()
    for u in base_vertices:
        for i in range(p):
            G.add_node((u, int(i)))

    for (u, v) in base_edges:
        pi = perms[(u, v)]
        for i in range(p):
            G.add_edge((u, int(i)), (v, int(pi[i])))

    return G


def sample_cycles(G: nx.Graph, L: int, max_cycles: int) -> list[tuple[tuple[int, int], ...]]:
    cycles: set[tuple[tuple[int, int], ...]] = set()
    node_ids = {node: idx for idx, node in enumerate(G.nodes())}
    for s in G.nodes():
        q = deque([(s, [s])])
        while q:
            v, path = q.popleft()
            if len(path) > L:
                continue
            for w in G.neighbors(v):
                if w == s and len(path) >= 3:
                    cyc = path + [s]
                    edges = []
                    for i in range(len(cyc) - 1):
                        a = node_ids[cyc[i]]
                        b = node_ids[cyc[i + 1]]
                        edges.append(tuple(sorted((a, b))))
                    cycles.add(tuple(sorted(edges)))
                    if len(cycles) >= max_cycles:
                        return list(cycles)
                if w not in path:
                    q.append((w, path + [w]))
    return list(cycles)


def incidence_matrix(G: nx.Graph, cycles: list[tuple[tuple[int, int], ...]]) -> np.ndarray:
    edge_list = [tuple(sorted(e)) for e in G.edges()]
    node_ids = {node: idx for idx, node in enumerate(G.nodes())}
    edge_list_int = [tuple(sorted((node_ids[u], node_ids[v]))) for (u, v) in edge_list]
    idx = {e: i for i, e in enumerate(edge_list_int)}
    M = np.zeros((len(cycles), len(edge_list_int)), dtype=np.uint8)
    for r, C in enumerate(cycles):
        for e in C:
            j = idx.get(e)
            if j is not None:
                M[r, j] = 1
    return M


def rank_f2(M: np.ndarray) -> int:
    M = (M.copy() % 2).astype(np.uint8)
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if M[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            M[[r, pivot]] = M[[pivot, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
        if r == rows:
            break
    return int(r)


def run_instance(p: int, L: int, max_cycles: int, seed: int) -> dict:
    G = random_lift_k4(p, seed)
    cycles = sample_cycles(G, L=L, max_cycles=max_cycles)
    M = incidence_matrix(G, cycles)
    r = rank_f2(M)
    n = G.number_of_nodes()
    m = G.number_of_edges()
    return {
        "family": "random_lift_K4",
        "p": p,
        "n": n,
        "m": m,
        "L": L,
        "max_cycles": max_cycles,
        "seed": seed,
        "cycles_sampled": len(cycles),
        "rank_F2": r,
        "rank_over_n": float(r / n),
        "rank_over_m": float(r / m),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p-values", type=int, nargs="+", default=[50, 100, 200, 400])
    ap.add_argument("--L", type=int, default=8)
    ap.add_argument("--max-cycles", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument(
        "--out",
        default="toolkit/oblivion/results/cycle_rank_random_lifts.json",
    )
    args = ap.parse_args()

    results = []
    for j, p in enumerate(args.p_values):
        res = run_instance(
            p=p,
            L=args.L,
            max_cycles=args.max_cycles,
            seed=args.seed + j,
        )
        print(res)
        results.append(res)

    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
