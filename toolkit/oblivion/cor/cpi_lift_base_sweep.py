#!/usr/bin/env python3

import json
import random
import networkx as nx

from toolkit.oblivion.cor.cycle_pair_interaction import cycle_pair_interaction_invariant


def random_lift(base_graph, lift_size, seed=0):
    rng = random.Random(seed)
    H = nx.Graph()
    for v in base_graph.nodes():
        for i in range(lift_size):
            H.add_node((v, i))
    for u, v in base_graph.edges():
        perm = list(range(lift_size))
        rng.shuffle(perm)
        for i in range(lift_size):
            H.add_edge((u, i), (v, perm[i]))
    return H


def theta_graph():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(1, 3)
    G.add_edge(0, 2)
    G.add_edge(2, 3)
    G.add_edge(0, 4)
    G.add_edge(4, 3)
    return G


def square_plus_diagonal():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 0)
    G.add_edge(0, 2)
    return G


def bowtie_graph():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 0)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 2)
    return G


def k4_graph():
    return nx.complete_graph(4)


def run():
    bases = {
        "theta": theta_graph(),
        "square_diag": square_plus_diagonal(),
        "bowtie": bowtie_graph(),
        "k4": k4_graph(),
    }

    out = []
    for name, base in bases.items():
        for m in [20, 40, 80]:
            G = random_lift(base, m, seed=1000 + m)
            inv = cycle_pair_interaction_invariant(G)
            inv["family"] = "random_lift"
            inv["base"] = name
            inv["lift_size"] = m
            out.append(inv)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
