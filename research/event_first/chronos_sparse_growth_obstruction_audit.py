#!/usr/bin/env python3
"""Exact, bounded audit of sparse random graph orders; no repository writes/deps.

Two models must not be conflated:
  ENSEMBLE: for each terminal N, every forward edge has p=lambda/N.
  SEQUENTIAL: edge into newly born j>=1 has p_j=min(1,lambda/j).
Run: python3 chronos_sparse_growth_obstruction_audit.py
"""
from fractions import Fraction as Q
from math import comb


def exact_exhaustive(n, p):
    """Enumerate all 2^(n choose 2) forward-edge sets and exact weights.
    Restricted to n<=5 to bound time/memory.
    """
    assert 3 <= n <= 5 and 0 <= p <= 1
    edges = [(i, j) for j in range(1, n) for i in range(j)]
    pair = chain = fork = Q(0)
    for mask in range(1 << len(edges)):
        rows = [0]*n
        for k, (i,j) in enumerate(edges):
            if (mask >> k) & 1:
                rows[i] |= 1 << j
        # Reverse-topological transitive closure (bitset algorithm).
        for i in range(n-1, -1, -1):
            for j in range(i+1,n):
                if (rows[i] >> j) & 1:
                    rows[i] |= rows[j]
        pair_count = sum(row.bit_count() for row in rows)
        chain_count = sum(bool((rows[i] >> j)&1 and (rows[j] >> k)&1)
                          for i in range(n) for j in range(i+1,n)
                          for k in range(j+1,n))
        fork_count = sum(bool(((rows[i]>>j)&1 and (rows[i]>>k)&1)
                             or ((rows[i]>>k)&1 and (rows[j]>>k)&1))
                         for i in range(n) for j in range(i+1,n)
                         for k in range(j+1,n))
        bits = mask.bit_count()
        weight = p**bits * (1-p)**(len(edges)-bits)
        pair += weight * Q(pair_count, comb(n,2))
        chain += weight * Q(chain_count, comb(n,3))
        fork += weight * Q(fork_count, comb(n,3))
    return pair, chain, fork


def path_union_pair_bound(n, p):
    """Independent exact upper bound via union of all directed paths."""
    return sum(Q(n-d,1) * p*(1+p)**(d-1)
               for d in range(1,n)) / comb(n,2)


def sparse_sequential_bound(n, lam, m):
    """Conservative exact path-union bound for integer lambda, labels 1..N.

    Early first vertices i<m contribute at most 2*(m-1)/N.
    For i>=m, any connection i->j has probability at most
      (lambda/j)*(j/i)^lambda <= lambda*N^lambda/m^(lambda+1).
    """
    assert 1 <= m < n and isinstance(lam,int) and lam > 0
    return Q(2*(m-1),n) + Q(lam*n**lam,m**(lam+1))

if __name__ == '__main__':
    lam = Q(2)
    for n in (3,4,5):
        p = lam/n
        measured = exact_exhaustive(n,p)
        bound = path_union_pair_bound(n,p)
        assert measured[0] <= bound
        # Basic monotonicity: chains and inclusive forks require comparable pairs.
        assert measured[1] <= measured[0] and measured[2] <= 3*measured[0]
        print(f'N={n} p={p} P2={measured[0]} P3={measured[1]} fork={measured[2]} path_bound={bound}')
    # Exact evidence that a birth-index-dependent p_j violates path independence
    # for equivalent unlabeled 3-element orders with one relation and one isolated vertex.
    p1, p2 = Q(1,2), Q(1,4)
    history_A = p1*(1-p2)**2 # edge 0->1, vertex 2 isolated
    history_B = p2*(1-p1)*(1-p2) # edge 0->2, vertex 1 isolated
    assert (history_A,history_B)==(Q(9,32),Q(3,32))
    print(f'LABEL_HISTORY_A={history_A} LABEL_HISTORY_B={history_B} EQUAL={history_A==history_B}')
    for n in (128,512,2048):
        m = round(n**0.75)
        print(f'SEQUENTIAL_N={n} lam=2 SPLIT={m} ANALYTICAL_BOUND={sparse_sequential_bound(n,2,m)}')
    print('FINITE_EXHAUSTIVE := PASS')
    print('ASYMPTOTIC_PATH_UNION_THEOREMS := ANALYTICAL_PROOF_NOT_LEAN_VERIFIED')
    print('REPO_EDITS := NONE')