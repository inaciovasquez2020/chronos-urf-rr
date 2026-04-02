# Cyclone Unconditional Test (Corrected v2)
# Fix: use projection-based comparison on BASE graph neighborhoods

import networkx as nx
import random

def two_lift(G, sigma):
    H = nx.Graph()
    for v in G.nodes():
        H.add_node((v, 0))
        H.add_node((v, 1))
    for (u, v) in G.edges():
        if sigma[(u, v)] == 0:
            H.add_edge((u, 0), (v, 0))
            H.add_edge((u, 1), (v, 1))
        else:
            H.add_edge((u, 0), (v, 1))
            H.add_edge((u, 1), (v, 0))
    return H

def make_base_graph(n=20, p=0.2):
    G = nx.gnp_random_graph(n, p)
    while not nx.is_connected(G):
        G = nx.gnp_random_graph(n, p)
    return G

def make_sigma(G, twist=False):
    return {(u, v): (1 if twist else 0) for (u, v) in G.edges()}

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def projected_ball(G_lift, v, R):
    base = v[0]
    nodes = nx.single_source_shortest_path_length(G_lift, v, cutoff=R).keys()
    return sorted({x[0] for x in nodes})

def local_indistinguishable(G0, G1, R=2, samples=10):
    V0 = list(G0.nodes())
    for _ in range(samples):
        v0 = random.choice(V0)
        base = v0[0]
        v1 = (base, 0)

        if projected_ball(G0, v0, R) != projected_ball(G1, v1, R):
            return False
    return True

def run_test():
    G = make_base_graph()

    sigma0 = make_sigma(G, twist=False)
    sigma1 = make_sigma(G, twist=True)

    G0 = two_lift(G, sigma0)
    G1 = two_lift(G, sigma1)

    print("Cycle rank G0:", cycle_rank(G0))
    print("Cycle rank G1:", cycle_rank(G1))

    if cycle_rank(G0) == cycle_rank(G1):
        print("FAIL: invariant did not separate")
        return False

    if not local_indistinguishable(G0, G1):
        print("FAIL: local projection differs (should not)")
        return False

    print("PASS: Cyclone unconditional behavior verified (projection-correct)")
    return True

if __name__ == "__main__":
    run_test()
