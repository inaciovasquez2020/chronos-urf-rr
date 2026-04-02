#!/usr/bin/env python3

from .cfi_pair_generator import cfi_pair_on_cycle
from .rooted_wl import wl_refinement

def wl_signature(G, R):
    return sorted(wl_refinement(G, v, R) for v in G)

def run():
    R = 2
    G0, G1 = cfi_pair_on_cycle(6, {(0,1)})
    sig0 = wl_signature(G0, R)
    sig1 = wl_signature(G1, R)

    print("WL_equal:", sig0 == sig1)
    print("types_G0:", len(set(sig0)))
    print("types_G1:", len(set(sig1)))

if __name__ == "__main__":
    run()
