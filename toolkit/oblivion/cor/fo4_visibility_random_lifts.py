#!/usr/bin/env python3

import json
import math

from toolkit.oblivion.cor.random_lift_cor_test import random_lift, base_theta_graph
from toolkit.oblivion.cor.cycle_overlap_rank import cycle_incidence_rank
from toolkit.oblivion.cor.fo4_visibility_proxy import pair_root_signature


def exhaustive_fo4_pair_stats(G, R=3):
    verts = list(G.nodes())
    freq = {}
    pair_count = 0

    for i, a in enumerate(verts):
        for b in verts[i + 1:]:
            s = pair_root_signature(G, a, b, R)
            freq[s] = freq.get(s, 0) + 1
            pair_count += 1

    distinct = len(freq)
    max_mult = max(freq.values()) if freq else 0

    return {
        "pairs_total": pair_count,
        "distinct_pair_signatures": distinct,
        "max_multiplicity": max_mult,
        "distinct_over_n": distinct / G.number_of_nodes(),
        "distinct_over_n2": distinct / (G.number_of_nodes() ** 2),
        "top10": dict(sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:10]),
    }


def run():
    base = base_theta_graph()
    out = []

    for m in [20, 40, 80, 120]:
        G = random_lift(base, m, seed=m)
        cor = cycle_incidence_rank(G)
        prox = exhaustive_fo4_pair_stats(G, R=3)

        out.append({
            "family": "theta_random_lift",
            "lift_size": m,
            "nodes": G.number_of_nodes(),
            "cor_rank": cor["rank"],
            "cor_rank_over_nodes": cor["rank"] / G.number_of_nodes(),
            "fo4_pair_distinct": prox["distinct_pair_signatures"],
            "fo4_pair_max_mult": prox["max_multiplicity"],
            "pairs_total": prox["pairs_total"],
            "fo4_pair_distinct_over_n": prox["distinct_over_n"],
            "fo4_pair_distinct_over_n2": prox["distinct_over_n2"],
        })

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
