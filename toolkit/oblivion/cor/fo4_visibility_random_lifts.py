#!/usr/bin/env python3

import json

from toolkit.oblivion.cor.random_lift_cor_test import random_lift, base_theta_graph
from toolkit.oblivion.cor.cycle_overlap_rank import cycle_incidence_rank
from toolkit.oblivion.cor.fo4_visibility_proxy import fo4_proxy_stats


def run():
    base = base_theta_graph()
    out = []
    for m in [20, 40, 80, 120]:
        G = random_lift(base, m, seed=m)
        cor = cycle_incidence_rank(G)
        prox = fo4_proxy_stats(G, R=3, max_pairs=4000)
        out.append({
            "family": "theta_random_lift",
            "lift_size": m,
            "nodes": G.number_of_nodes(),
            "cor_rank": cor["rank"],
            "cor_rank_over_nodes": cor["rank"] / G.number_of_nodes(),
            "fo4_pair_distinct": prox["distinct_pair_signatures"],
            "fo4_pair_max_mult": prox["max_multiplicity"],
            "pairs_sampled": prox["pairs_sampled"],
        })
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
