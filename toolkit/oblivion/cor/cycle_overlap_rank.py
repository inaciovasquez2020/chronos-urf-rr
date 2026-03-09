#!/usr/bin/env python3

import networkx as nx
import numpy as np


def cycle_incidence_rank(G):
    """
    Compute cycle–edge incidence rank over F2 using the cycle basis.
    Returns:
        rank
        matrix_shape
        number_of_cycles
        number_of_edges
    """

    cycles = nx.cycle_basis(G)

    edges = list(G.edges())
    edge_index = {}

    for i,e in enumerate(edges):
        edge_index[e] = i
        edge_index[(e[1],e[0])] = i

    A = np.zeros((len(cycles), len(edges)), dtype=np.int8)

    for i,cycle in enumerate(cycles):

        for j in range(len(cycle)):

            u = cycle[j]
            v = cycle[(j+1) % len(cycle)]

            idx = edge_index.get((u,v))

            if idx is None:
                idx = edge_index[(v,u)]

            A[i,idx] = 1

    rank = np.linalg.matrix_rank(A % 2)

    return {
        "rank": int(rank),
        "matrix_shape": A.shape,
        "cycles": len(cycles),
        "edges": len(edges)
    }


def random_regular_test(n=200, d=4, seed=1):

    G = nx.random_regular_graph(d, n, seed=seed)

    res = cycle_incidence_rank(G)

    res["n"] = n
    res["degree"] = d
    res["rank_over_n"] = res["rank"] / n

    return res


def cayley_cycle_graph(n):

    G = nx.Graph()

    for i in range(n):
        G.add_edge(i, (i+1) % n)
        G.add_edge(i, (i+2) % n)

    return G


def cayley_test(n=200):

    G = cayley_cycle_graph(n)

    res = cycle_incidence_rank(G)

    res["n"] = n
    res["graph"] = "cayley_cycle"
    res["rank_over_n"] = res["rank"] / n

    return res


def scaling_experiment():

    sizes = [200, 400, 800, 1200]

    results = []

    for n in sizes:

        r = random_regular_test(n)

        results.append(r)

    return results


def continuum_constant(results):

    ratios = [r["rank_over_n"] for r in results]

    return min(ratios)


def main():

    print("=== RANDOM REGULAR TEST ===")
    r = random_regular_test()
    print(r)

    print("\n=== CAYLEY TEST ===")
    c = cayley_test()
    print(c)

    print("\n=== SCALING TEST ===")
    s = scaling_experiment()

    for x in s:
        print(x)

    print("\n=== CONTINUUM CONSTANT ESTIMATE ===")
    C = continuum_constant(s)
    print("C_estimate =", C)


if __name__ == "__main__":
    main()
