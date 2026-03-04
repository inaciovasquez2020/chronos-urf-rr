# experiments/cycle_overlap/random_lift_CR_test.py

import networkx as nx
from compute_CR import compute_CR

def base_graph():
    return nx.complete_graph(4)

def random_lift(base, n):
    return nx.algorithms.lifted_graph.lift(base, n)

def run():
    R = 2
    base = base_graph()

    print("\n=== RANDOM LIFT TEST ===")

    for n in [10, 20, 40, 80, 160]:
        G = random_lift(base, n)
        CR = compute_CR(G, R)
        print("lift n=", n, "CR=", CR)

if __name__ == "__main__":
    run()
