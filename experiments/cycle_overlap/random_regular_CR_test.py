# experiments/cycle_overlap/random_regular_CR_test.py

import networkx as nx
from compute_CR import compute_CR

def random_regular_graph(n, d):
    return nx.random_regular_graph(d, n)

def run():
    R = 2
    d = 4

    print("\n=== RANDOM REGULAR TEST ===")

    for n in [100, 200, 400, 800, 1600]:
        G = random_regular_graph(n, d)
        CR = compute_CR(G, R)
        print("n=", n, "CR=", CR)

if __name__ == "__main__":
    run()
