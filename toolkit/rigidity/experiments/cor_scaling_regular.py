import networkx as nx
import numpy as np
import json
from pathlib import Path

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
    return int(np.linalg.matrix_rank(O))

def run_scaling(n_values, d, trials):
    results = []
    for n in n_values:
        for t in range(trials):
            G = nx.random_regular_graph(d, n)
            cor = cycle_overlap_rank(G)
            results.append({
                "n": n,
                "degree": d,
                "trial": t,
                "cor": cor
            })
            print("n=",n,"trial=",t,"COR=",cor)
    return results

if __name__ == "__main__":
    n_values = [40,60,80,100,150,200]
    d = 3
    trials = 10

    results = run_scaling(n_values,d,trials)

    Path("results").mkdir(exist_ok=True)
    with open("results/cor_scaling_regular.json","w") as f:
        json.dump(results,f,indent=2)
