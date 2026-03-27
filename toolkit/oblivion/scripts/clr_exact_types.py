#!/usr/bin/env python3

from rooted_iso import rooted_iso
from clr_cayley_homogeneous_test import cayley_cycle, cayley_grid

def count_types(G, R):
    reps = []
    for v in G:
        found = False
        for r in reps:
            if rooted_iso(G, v, r, R):
                found = True
                break
        if not found:
            reps.append(v)
    return len(reps)

def run():
    R = 2

    for n in [6,8,10]:
        G = cayley_cycle(n)
        print("cycle", n, count_types(G,R))

    for n in [4,6]:
        G = cayley_grid(n)
        print("grid", n, count_types(G,R))

if __name__ == "__main__":
    run()
