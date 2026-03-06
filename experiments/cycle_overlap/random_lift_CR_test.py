# experiments/cycle_overlap/random_lift_CR_test.py

import networkx as nx
import random
from compute_CR import compute_CR


def base_graph():
    return nx.complete_graph(4)


def random_lift(base, k):
    """
    k-lift of base graph using random permutations.
    """
    G = nx.Graph()

    for v in base.nodes():
        for i in range(k):
            G.add_node((v, i))

    for (u, v) in base.edges():
        perm = list(range(k))
        random.shuffle(perm)
        for i in range(k):
            G.add_edge((u, i), (v, perm[i]))

    return nx.convert_node_labels_to_integers(G)


def run():
    R = 3
    R = 4
    base = base_graph()

    print("\n=== RANDOM LIFT TEST ===")

    for k in [10, 20, 40, 80]:
        G = random_lift(base, k)
        CR = compute_CR(G, R)
        print("lift size=", k, "CR=", CR)


if __name__ == "__main__":
    run()
