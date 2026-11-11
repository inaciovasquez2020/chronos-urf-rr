#!/usr/bin/env python3
"""Finite ordinal-sum chain/fork collision; bounded computational audit only."""
import itertools
import math

if not __debug__:
    raise SystemExit("INCOMPLETE: optimized Python disables asserts")

def compositions(n):
    if n == 0:
        yield ()
        return
    for first in range(1, n + 1):
        for rest in compositions(n - first):
            yield (first,) + rest

def direct_signature(sizes):
    levels = tuple(i for i, count in enumerate(sizes) for _ in range(count))
    n = len(levels)
    chains = tuple(
        sum(len({levels[v] for v in chosen}) == k
            for chosen in itertools.combinations(range(n), k))
        for k in range(1, n + 1)
    )
    forks = sum(
        levels[x] < levels[y] == levels[z]
        for x in range(n)
        for y, z in itertools.combinations(range(n), 2)
    )
    return chains, forks

def formula_signature(sizes):
    polynomial = [1]
    for a in sizes:
        new = [0] * (len(polynomial) + 1)
        for i, coefficient in enumerate(polynomial):
            new[i] += coefficient
            new[i + 1] += a * coefficient
        polynomial = new
    n = sum(sizes)
    polynomial += [0] * (n + 1 - len(polynomial))
    earlier = forks = 0
    for a in sizes:
        forks += earlier * math.comb(a, 2)
        earlier += a
    return tuple(polynomial[1:]), forks

summary = []
for n in range(1, 7):
    signatures = {}
    collisions = []
    for sizes in compositions(n):
        direct = direct_signature(sizes)
        formula = formula_signature(sizes)
        if direct != formula:
            raise AssertionError(("INDEPENDENT_MISMATCH", sizes, direct, formula))
        if direct in signatures:
            collisions.append((signatures[direct], sizes, direct))
        else:
            signatures[direct] = sizes
    summary.append((n, 2 ** (n - 1), len(signatures), len(collisions)))
    if n < 6 and collisions:
        raise AssertionError(("UNEXPECTED_EARLY_COLLISION", n, collisions))
    if n == 6 and collisions != [
        ((1, 2, 2, 1), (2, 1, 1, 2), ((6, 13, 12, 4, 0, 0), 4))
    ]:
        raise AssertionError(("WRONG_COLLISION_SET", collisions))

if (1, 2, 2, 1)[0] == (2, 1, 1, 2)[0]:
    raise AssertionError("NONISOMORPHISM_WITNESS_BAD")

print("COMPOSITIONS_AUDITED :=", sum(2 ** (n - 1) for n in range(1, 7)))
print("PER_EVENT_COUNTS :=", summary)
print("CHAIN_COUNTS := (6, 13, 12, 4, 0, 0); FORKS := 4")
print("RESULT := COMPUTATION_PASS")
print("PROOF_STATUS := PAPER_ARGUMENT; LEAN_VERIFIED := NOT_RUN; SPACETIME_EMERGENCE := OPEN")
