#!/usr/bin/env python3

from clr_local_transition_scan import random_n_lift, connected_regular_base, cycle_rank
from rooted_wl import count_types_wl

def run_test():
    R = 2
    d = 3
    base = connected_regular_base(d)

    for n in [4, 8, 12, 16, 20]:
        G = random_n_lift(base, n=n, seed=42 + n)
        types = count_types_wl(G, R)
        print(f"lift n={n}, wl_types={types}, cycle_rank={cycle_rank(G)}")

if __name__ == "__main__":
    run_test()
