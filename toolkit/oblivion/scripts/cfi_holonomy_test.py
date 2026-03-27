#!/usr/bin/env python3

from .cfi_pair_generator import cfi_labeled_pair_on_cycle


def holonomy_phi(G_labeled, n):
    acc = 0
    for v in range(n):
        u = (v + 1) % n
        label = G_labeled.get((v, 0), {}).get((u, 0), 0) or \
                G_labeled.get((v, 0), {}).get((u, 1), 0)
        acc ^= label
    return acc
