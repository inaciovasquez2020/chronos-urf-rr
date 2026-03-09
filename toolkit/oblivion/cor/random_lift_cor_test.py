#!/usr/bin/env python3

import json
import random
import networkx as nx

from toolkit.oblivion.cor.cycle_overlap_rank import cycle_incidence_rank


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


def base_theta_graph():
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(1, 3)
    G.add_edge(0, 2)
    G.add_edge(2, 3)
    G.add_edge(0, 4)
    G.add_edge(4, 3)
    return G


def run():
    base = base_theta_graph()
    out = []
    for n in [20, 40, 80, 120]:
        G = random_lift(base, n, seed=n)
        res = cycle_incidence_rank(G)
        res["lift_size"] = n
        res["nodes"] = G.number_of_nodes()
        res["edges"] = G.number_of_edges()
        res["rank_over_nodes"] = res["rank"] / G.number_of_nodes()
        out.append(res)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
