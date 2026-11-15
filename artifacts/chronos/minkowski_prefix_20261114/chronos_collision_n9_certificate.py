#!/usr/bin/env python3
"""Read-only exact exhaustive audit of uniformly random 2D permutation posets.
No repo files or external dependencies; Python >= 3.9.
"""
import itertools, math, sys, time
from functools import lru_cache

def evaluate(p):
    n = len(p)
    predecessors = [sum(1 << i for i in range(j) if p[i] < p[j]) for j in range(n)]
    full = (1 << n) - 1
    @lru_cache(None)
    def extensions(mask):
        if not mask:
            return 1
        return sum(extensions(mask ^ (1 << i)) for i in range(n)
                   if mask & (1 << i) and not (predecessors[i] & mask))
    e = extensions(full)
    minima = [i for i in range(n) if predecessors[i] == 0]
    first = [extensions(full ^ (1 << i)) for i in minima]
    assert sum(first) == e
    chain_prefix = sum(extensions(full ^ (1 << i) ^ (1 << j))
                       for i in minima for j in range(n)
                       if predecessors[j] == (1 << i))
    collision_num = sum(x*x for x in first)
    assert 0 <= chain_prefix <= e
    assert (n-1)*chain_prefix*e <= n*collision_num-e*e, (p, 'Fishburn bound failed')
    return chain_prefix/e, collision_num/(e*e), max(first)/e

def main():
    n = int(sys.argv[1]) if len(sys.argv)>1 else 9
    if not 2 <= n <= 9:
        raise SystemExit('Guard: n must be in 2..9; otherwise audit is deliberately incomplete')
    s = [0.0, 0.0, 0.0]
    t0 = time.monotonic()
    for p in itertools.permutations(range(n)):
        a,c,m = evaluate(p)
        s[0] += a; s[1] += c; s[2] += m
    total = math.factorial(n)
    print('RESULT := COMPUTATION_PASS')
    print('MODEL := all permutations of length', n, '(uniform random 2D order)')
    print('COUNT :=', total)
    print('FINITE_PREFIX_MEAN := %.12f' % (s[0]/total))
    print('COLLISION_MEAN := %.12f' % (s[1]/total))
    print('MAX_FIRST_PROB_MEAN := %.12f' % (s[2]/total))
    print('INVARIANTS := extension normalization and integer Fishburn bound PASS for every permutation')
    print('ASYMPTOTIC_CONCLUSION := OPEN')
    print('ELAPSED_SECONDS := %.3f' % (time.monotonic()-t0))
if __name__=='__main__': main()