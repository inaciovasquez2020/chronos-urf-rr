# experiments/cycle_overlap/compute_CR.py

import networkx as nx
import numpy as np


def cycle_basis_edges(G, nodes):
    """
    Compute cycle basis of the induced subgraph on `nodes`
    and return cycles as lists of undirected edges.
    """
    H = G.subgraph(nodes)
    basis = nx.cycle_basis(H)

    cycles = []
    for c in basis:
        edges = []
        for i in range(len(c)):
            u = c[i]
            v = c[(i + 1) % len(c)]
            if G.has_edge(u, v):
                edges.append(tuple(sorted((u, v))))
        cycles.append(edges)

    return cycles


def incidence_vector(edges, edge_index):
    """
    Convert list of edges into a binary incidence vector over E(G).
    """
    v = np.zeros(len(edge_index), dtype=np.uint8)

    for e in edges:
        if e in edge_index:
            v[edge_index[e]] ^= 1

    return v


def rank_mod2(M):
    """
    Compute rank over F2 using Gaussian elimination.
    """
    M = M.copy()
    r = 0
    rows, cols = M.shape

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

    return r


def compute_CR(G, R):
    """
    Compute C_R(G) = rank_F2(Im Φ_R)
    by collecting cycle bases of all radius-R balls.
    """

    edges = [tuple(sorted(e)) for e in G.edges()]
    edge_index = {e: i for i, e in enumerate(edges)}

    rows = []

    for v in G.nodes():

        nodes = nx.single_source_shortest_path_length(
            G, v, cutoff=R
        ).keys()

        cycles = cycle_basis_edges(G, nodes)

        for c in cycles:
            rows.append(incidence_vector(c, edge_index))

    if len(rows) == 0:
        return 0

    M = np.vstack(rows)

    return rank_mod2(M)


def torus_graph(n):
    """
    2D torus grid graph.
    """
    G = nx.grid_2d_graph(n, n, periodic=True)
    return nx.convert_node_labels_to_integers(G)


def ladder_graph(n):
    """
    Ladder graph.
    """
    return nx.ladder_graph(n)


def run_experiments():

    print("\n=== TORUS TEST ===")

    for n in [10, 20, 40, 80]:
        G = torus_graph(n)
        CR = compute_CR(G, 2)
        print("torus n=", n, "CR=", CR)

    print("\n=== LADDER TEST ===")

    for n in [10, 20, 40, 80]:
        G = ladder_graph(n)
        CR = compute_CR(G, 2)
        print("ladder n=", n, "CR=", CR)


if __name__ == "__main__":
    run_experiments()
