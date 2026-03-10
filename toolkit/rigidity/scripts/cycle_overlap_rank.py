import networkx as nx
import numpy as np
from itertools import combinations

def cycle_basis(G):
    return nx.cycle_basis(G)

def incidence_matrix(G, cycles):
    edges = list(G.edges())
    edge_index = {tuple(sorted(e)): i for i,e in enumerate(edges)}
    A = np.zeros((len(edges), len(cycles)), dtype=int)

    for j,C in enumerate(cycles):
        for i in range(len(C)):
            e = tuple(sorted((C[i], C[(i+1)%len(C)])))
            A[edge_index[e], j] = 1

    return A

def cycle_overlap_rank(G):
    cycles = cycle_basis(G)
    if len(cycles) == 0:
        return 0

    A = incidence_matrix(G, cycles)
    O = A.T @ A
    return np.linalg.matrix_rank(O)

def test_random_graph(n=40, d=3, trials=10):
    for t in range(trials):
        G = nx.random_regular_graph(d, n)
        cor = cycle_overlap_rank(G)
        print(f"trial={t}  COR={cor}")

if __name__ == "__main__":
    test_random_graph()
