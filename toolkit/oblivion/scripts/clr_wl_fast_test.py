#!/usr/bin/env python3

from rooted_wl import count_types_wl
from clr_cayley_homogeneous_test import cayley_cycle, cayley_grid

def run():
    R = 2

    for n in [6,8,10]:
        G = cayley_cycle(n)
        print("cycle", n, count_types_wl(G,R))

    for n in [4,6,8]:
        G = cayley_grid(n)
        print("grid", n, count_types_wl(G,R))

if __name__ == "__main__":
    run()
