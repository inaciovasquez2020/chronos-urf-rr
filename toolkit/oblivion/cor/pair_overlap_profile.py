#!/usr/bin/env python3

import json

from toolkit.oblivion.cor.random_lift_cor_test import random_lift, base_theta_graph
from toolkit.oblivion.cor.fo4_visibility_proxy import pair_root_signature


def pair_overlap_profile(G, R=3):
    verts = list(G.nodes())
    freq = {}
    total_pairs = 0

    for i, a in enumerate(verts):
        for b in verts[i + 1:]:
            s = pair_root_signature(G, a, b, R)
            freq[s] = freq.get(s, 0) + 1
            total_pairs += 1

    mults = sorted(freq.values(), reverse=True)

    return {
        "pairs_total": total_pairs,
        "distinct_pair_signatures": len(freq),
        "max_multiplicity": mults[0] if mults else 0,
        "top_multiplicities": mults[:20],
        "histogram_of_multiplicities": {
            str(k): v for k, v in sorted(_histogram(mults).items())
        },
    }


def _histogram(values):
    out = {}
    for x in values:
        out[x] = out.get(x, 0) + 1
    return out


def run():
    base = base_theta_graph()
    out = []

    for m in [20, 40, 80, 120]:
        G = random_lift(base, m, seed=m)
        prof = pair_overlap_profile(G, R=3)
        prof["family"] = "theta_random_lift"
        prof["lift_size"] = m
        prof["nodes"] = G.number_of_nodes()
        out.append(prof)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
