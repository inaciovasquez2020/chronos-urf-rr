# experiments/cycle_overlap/high_cycle_overlap_test.py

import networkx as nx
from compute_CR import compute_CR


def triangular_lattice(n):
    G = nx.Graph()
    for x in range(n):
        for y in range(n):
            v = (x, y)
            nbrs = [
                ((x+1)%n, y),
                (x, (y+1)%n),
                ((x+1)%n, (y-1)%n)
            ]
            for u in nbrs:
                G.add_edge(v, u)
    return nx.convert_node_labels_to_integers(G)


def run():
    R = 2
    print("\n=== HIGH OVERLAP TEST ===")

    for n in [10,20,40,80]:
        G = triangular_lattice(n)
        CR = compute_CR(G, R)
        print("triangular n=", n, "CR=", CR)


if __name__ == "__main__":
    run()
