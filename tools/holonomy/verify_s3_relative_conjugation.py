#!/usr/bin/env python3
"""Exact finite S3 global-versus-independent-local holonomy orbit audit.

Model: k fundamental loops based at one root. Global gauge acts by ONE
simultaneous conjugation; each local loop observation is conjugacy-quotiented
INDEPENDENTLY. Intended geometric realization: separated loops with distinct
radius-r observation balls and no overlap transition-gauge observations.
No claim about full Chronos graph-ball or 5D physical necessity.
"""
from collections import defaultdict
from itertools import permutations, product

if not __debug__:
    raise SystemExit("OPTIMIZED_EXECUTION_REJECTED")

S3 = tuple(permutations(range(3)))

def mul(a, b):
    return tuple(a[b[i]] for i in range(3))

def inv(a):
    return tuple(a.index(i) for i in range(3))

def conj(g, x):
    return mul(mul(g, x), inv(g))

def global_canon(x):
    return min(tuple(conj(g, z) for z in x) for g in S3)

def local_signature(x):
    return tuple(min(conj(g, z) for g in S3) for z in x)

def centralizer_size(g):
    return sum(mul(g, x) == mul(x, g) for x in S3)

def test():
    assert len(S3) == 6
    sizes = sorted(centralizer_size(g) for g in S3)
    assert sizes == [2, 2, 2, 3, 3, 6]
    expected_counts = {1: (3, 3), 2: (11, 9),
                       3: (49, 27), 4: (251, 81)}
    total_assignments = 0
    for k, (ng, nl) in expected_counts.items():
        fibers = defaultdict(set)
        for x in product(S3, repeat=k):
            fibers[local_signature(x)].add(global_canon(x))
            total_assignments += 1
        global_count = sum(map(len, fibers.values()))
        burnside = sum(centralizer_size(g)**k for g in S3) // len(S3)
        assert global_count == burnside == ng
        assert len(fibers) == nl == 3**k
        assert all(len(v) >= 1 for v in fibers.values())
        print(f"LOOPS={k} ASSIGNMENTS={6**k} GLOBAL={ng} LOCAL={nl} "
              f"MAX_FIBER={max(map(len, fibers.values()))} PASS")
    a, b = (1, 0, 2), (0, 2, 1)
    assert local_signature((a, a)) == local_signature((a, b))
    assert global_canon((a, a)) != global_canon((a, b))
    assert total_assignments == 1554
    print("EXPLICIT_NONABELIAN_COLLISION := PASS")
    print("TOTAL_ASSIGNMENTS := 1554")
    print("LEAN_VERIFIED := NOT_RUN; PHYSICAL_5D_NECESSITY := OPEN")

if __name__ == "__main__":
    test()
