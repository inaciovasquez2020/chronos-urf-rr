#!/usr/bin/env python3

from collections import defaultdict
from .clr_local_transition_scan import type_set, cycle_rank

def cayley_cycle(n: int):
    G = defaultdict(set)
    for i in range(n):
        G[i].add((i+1) % n)
        G[(i+1) % n].add(i)
    return G

def cayley_grid(n: int):
    G = defaultdict(set)
    def vid(x,y): return x*n + y
    for x in range(n):
        for y in range(n):
            u = vid(x,y)
            v1 = vid((x+1)%n, y)
            v2 = vid(x, (y+1)%n)
            G[u].add(v1); G[v1].add(u)
            G[u].add(v2); G[v2].add(u)
    return G

def run_test():
    R = 2

    for n in [6, 8, 10, 12]:
        G = cayley_cycle(n)
        types = type_set(G, R)
        print(f"cycle n={n}, types={len(types)}, rank={cycle_rank(G)}")

    for n in [4, 6, 8, 10]:
        G = cayley_grid(n)
        types = type_set(G, R)
        print(f"grid n={n}, types={len(types)}, rank={cycle_rank(G)}")

if __name__ == "__main__":
    run_test()
