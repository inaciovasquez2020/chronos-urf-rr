#!/usr/bin/env python3

import json
import networkx as nx

from toolkit.oblivion.cor.cycle_pair_interaction import cycle_pair_interaction_invariant


def filtered_random_regular(degree, n, girth_min, trials=100):
    best = None
    best_girth = -1
    for seed in range(trials):
        G = nx.random_regular_graph(degree, n, seed=seed)
        cycles = nx.cycle_basis(G)
        girth = min((len(c) for c in cycles), default=float("inf"))
        if girth > best_girth:
            best = G
            best_girth = girth
        if girth >= girth_min:
            return G, girth
    return best, best_girth


def run():
    out = []
    for n in [100, 200, 300, 400]:
        G, girth = filtered_random_regular(3, n, girth_min=8, trials=200)
        inv = cycle_pair_interaction_invariant(G)
        inv["family"] = "high_girth_rr3"
        inv["n"] = n
        inv["girth"] = girth
        out.append(inv)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
