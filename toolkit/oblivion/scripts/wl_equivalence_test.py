#!/usr/bin/env python3

from .rooted_wl import wl_refinement

def wl_signature(G, R):
    return sorted(wl_refinement(G, v, R) for v in G)

def small_pair():
    G0 = {
        0:{1},1:{0,2},2:{1}
    }
    G1 = {
        0:{1,2},1:{0,2},2:{0,1}
    }
    return G0, G1

def run():
    R = 2
    G0, G1 = small_pair()

    sig0 = wl_signature(G0, R)
    sig1 = wl_signature(G1, R)

    print("WL equal:", sig0 == sig1)

if __name__ == "__main__":
    run()
