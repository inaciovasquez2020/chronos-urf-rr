#!/usr/bin/env python3

from clr_local_transition_scan import random_n_lift, connected_regular_base, type_set, cycle_rank

def run_test():
    R = 2
    d = 3
    base = connected_regular_base(d)

    for n in [4, 8, 12, 16, 20]:
        G = random_n_lift(base, n=n, seed=42+n)
        types = type_set(G, R)

        if len(types) == 1:
            print(f"PASS: homogeneous lift n={n}, cycle_rank={cycle_rank(G)}")
        else:
            print(f"FAIL: non-homogeneous lift n={n}, types={len(types)}")

if __name__ == "__main__":
    run_test()
