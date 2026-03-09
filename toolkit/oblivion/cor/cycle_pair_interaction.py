#!/usr/bin/env python3

import json
import networkx as nx
import numpy as np


def _normalize_edge(u, v):
    return (u, v) if u <= v else (v, u)


def cycle_basis_edges(G):
    basis = nx.cycle_basis(G)
    edge_cycles = []
    for cyc in basis:
        edges = []
        m = len(cyc)
        for i in range(m):
            u = cyc[i]
            v = cyc[(i + 1) % m]
            edges.append(_normalize_edge(u, v))
        edge_cycles.append(tuple(sorted(edges)))
    return edge_cycles


def cycle_edge_incidence_matrix(G):
    cycles = cycle_basis_edges(G)
    edges = sorted(_normalize_edge(u, v) for u, v in G.edges())
    edge_index = {e: i for i, e in enumerate(edges)}

    A = np.zeros((len(cycles), len(edges)), dtype=np.uint8)
    for i, cyc in enumerate(cycles):
        for e in cyc:
            A[i, edge_index[e]] = 1
    return A, cycles, edges


def gf2_rank(A):
    M = (A.copy() % 2).astype(np.uint8)
    m, n = M.shape
    r = 0
    c = 0
    while r < m and c < n:
        pivot = None
        for i in range(r, m):
            if M[i, c]:
                pivot = i
                break
        if pivot is None:
            c += 1
            continue
        if pivot != r:
            M[[r, pivot]] = M[[pivot, r]]
        for i in range(m):
            if i != r and M[i, c]:
                M[i, :] ^= M[r, :]
        r += 1
        c += 1
    return int(r)


def cycle_intersection_graph_matrix(G):
    cycles = cycle_basis_edges(G)
    m = len(cycles)
    B = np.zeros((m, m), dtype=np.uint8)

    cycle_sets = [set(c) for c in cycles]
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            if cycle_sets[i].intersection(cycle_sets[j]):
                B[i, j] = 1
    return B, cycles


def cycle_pair_interaction_matrix(G):
    cycles = cycle_basis_edges(G)
    m = len(cycles)
    if m == 0:
        return np.zeros((0, 0), dtype=np.uint8), cycles

    cycle_sets = [set(c) for c in cycles]
    P = np.zeros((m, m), dtype=np.uint8)

    for i in range(m):
        for j in range(i + 1, m):
            inter = cycle_sets[i].intersection(cycle_sets[j])
            P[i, j] = len(inter) % 2
            P[j, i] = P[i, j]
    return P, cycles


def cycle_pair_interaction_invariant(G):
    A, cycles_A, edges = cycle_edge_incidence_matrix(G)
    B, cycles_B = cycle_intersection_graph_matrix(G)
    P, cycles_P = cycle_pair_interaction_matrix(G)

    assert len(cycles_A) == len(cycles_B) == len(cycles_P)

    rank_A = gf2_rank(A) if A.size else 0
    rank_B = gf2_rank(B) if B.size else 0
    rank_P = gf2_rank(P) if P.size else 0

    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "cycle_basis_size": len(cycles_A),
        "cycle_edge_rank": rank_A,
        "cycle_intersection_rank": rank_B,
        "cycle_pair_interaction_rank": rank_P,
        "cycle_edge_rank_over_n": (rank_A / G.number_of_nodes()) if G.number_of_nodes() else 0.0,
        "cycle_intersection_rank_over_n": (rank_B / G.number_of_nodes()) if G.number_of_nodes() else 0.0,
        "cycle_pair_interaction_rank_over_n": (rank_P / G.number_of_nodes()) if G.number_of_nodes() else 0.0,
    }


def run_random_regular():
    out = []
    for n in [200, 400, 800]:
        G = nx.random_regular_graph(4, n, seed=n)
        inv = cycle_pair_interaction_invariant(G)
        inv["family"] = "random_regular_4"
        inv["n"] = n
        out.append(inv)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run_random_regular()
