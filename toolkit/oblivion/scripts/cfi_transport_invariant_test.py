#!/usr/bin/env python3

from cfi_pair_generator import cfi_pair_on_cycle

def edge_parity_signature(G):
    sig = 0
    for v in G:
        sig ^= len(G[v]) % 2
    return sig

def transport_invariant(G):
    total = 0
    for v in G:
        for u in G[v]:
            if v < u:
                total += (len(G[v]) - len(G[u]))**2
    return total

def run():
    G0, G1 = cfi_pair_on_cycle(6, {(0,1)})

    print("parity G0:", edge_parity_signature(G0))
    print("parity G1:", edge_parity_signature(G1))

    print("transport G0:", transport_invariant(G0))
    print("transport G1:", transport_invariant(G1))

if __name__ == "__main__":
    run()
