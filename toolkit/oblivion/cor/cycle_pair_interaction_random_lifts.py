#!/usr/bin/env python3

import json

from toolkit.oblivion.cor.random_lift_cor_test import random_lift, base_theta_graph
from toolkit.oblivion.cor.cycle_pair_interaction import cycle_pair_interaction_invariant


def run():
    base = base_theta_graph()
    out = []

    for m in [20, 40, 80, 120]:
        G = random_lift(base, m, seed=m)
        inv = cycle_pair_interaction_invariant(G)
        inv["family"] = "theta_random_lift"
        inv["lift_size"] = m
        out.append(inv)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
