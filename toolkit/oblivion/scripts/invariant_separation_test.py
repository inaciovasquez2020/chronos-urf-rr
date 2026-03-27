#!/usr/bin/env python3

from rooted_wl import wl_refinement
from clr_local_transition_scan import cycle_rank

def I(G, R):
    counts = {}
    for v in G:
        t = wl_refinement(G, v, R)
        counts.setdefault(t, 0)
        counts[t] += 1
    return sum(m * (len(t)**2) for t, m in counts.items())

def small_twist_pair():
    # placeholder: two graphs with same WL but different structure
    G0 = {0:{1},1:{0,2},2:{1}}
    G1 = {0:{1},1:{0,2},2:{1}}  # replace with real CFI pair later
    return G0, G1

def run():
    R = 2
    G0, G1 = small_twist_pair()

    print("I(G0) =", I(G0,R))
    print("I(G1) =", I(G1,R))
    print("cycle ranks:", cycle_rank(G0), cycle_rank(G1))

if __name__ == "__main__":
    run()
