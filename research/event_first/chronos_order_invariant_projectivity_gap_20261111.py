#!/usr/bin/env python3
"""Exact two-/three-stage order-invariant Minkowski projectivity gap.
Only stdlib. Deterministic, read-only; checks the finite-stage minimax bound.
"""
from fractions import Fraction as F
from itertools import permutations

SHAPES = {
    'chain': ((0,1),(1,2)),
    'fork': ((0,2),(1,2)),
    'merge': ((0,1),(0,2)),
    'single': ((0,1),),
    'antichain': (),
}

def pair_probability(edges):
    rel = [[False]*3 for _ in range(3)]
    for a,b in edges: rel[a][b]=True
    for k in range(3):
        for i in range(3):
            for j in range(3):
                rel[i][j] |= rel[i][k] and rel[k][j]
    extensions = [v for v in permutations(range(3))
                  if all(v.index(a)<v.index(b) for a,b in edges)]
    return F(sum(rel[v[0]][v[1]] for v in extensions),len(extensions)),len(extensions)

# Volumetric 4D Minkowski two-/three-point identities independently encoded
# as exact known moments. They are input, not numerical approximations.
E_S, E_S2, E_SF = F(1,20), F(1,105), F(1,2100)
q3 = {'chain':6*E_SF,
      'fork':3*(E_S2-2*E_SF),
      'merge':3*(E_S2-2*E_SF)}
q3['single'] = 3*(2*E_S)-3*q3['chain']-2*(q3['fork']+q3['merge'])
q3['antichain'] = 1-sum(q3.values())
assert sum(q3.values()) == 1 and all(v>=0 for v in q3.values())
T = {s:pair_probability(edges)[0] for s,edges in SHAPES.items()}
assert T == {'chain':F(1), 'fork':F(0), 'merge':F(1),
             'single':F(1,3), 'antichain':F(0)}

def project(q): return sum((q[s]*T[s] for s in SHAPES),F(0))

def tv(q,r): return sum((abs(q[s]-r[s]) for s in q),F(0))/2

q2 = F(1,10)
tq3 = project(q3)
defect = abs(q2-tq3)
assert tq3 == F(16,175) and defect == F(3,350)

# For any law nu3 on 3-element posets, order-invariance gives
# nu2 = T(nu3), hence TV(Q2,TQ3) <= TV(Q2,nu2)+TV(nu3,Q3).
# The minimax discrepancy is >= defect/2. Attain it for these two levels:
shift = defect/2
nu3 = dict(q3)
nu3['antichain'] -= shift
nu3['merge'] += shift
assert all(x>=0 for x in nu3.values()) and sum(nu3.values()) == 1
nu2 = project(nu3)
err2 = abs(nu2-q2)
err3 = tv(nu3,q3)
assert err2 == err3 == shift == F(3,700)
assert all(F(0)<=s<=F(1) for s in T.values())
print('Q3_TYPES :=',q3)
print('LINEAR_EXTENSION_PREFIX_PROBABILITIES :=',T)
print('FRESH_Q2_COMPARABLE :=',q2)
print('T_Q3_COMPARABLE :=',tq3)
print('EXACT_PROJECTIVITY_DEFECT_TV :=',defect)
print('MINIMAX_LOWER_BOUND_MAX_TV_STAGE_2_OR_3 :=',shift)
print('FINITE_TWO_STAGE_ATTAINABILITY := PASS')
print('MODIFIED_THREE_EVENT_LAW :=',nu3)
print('FINITE_PREFIX_LAW_COMPARABLE :=',nu2)
print('ALL_STAGE_FRESH_MINKOWSKI_PROJECTIVITY := IMPOSSIBLE')
print('LARGE_PREFIX_UNIFORM_SUBSET_MINKOWSKI := OPEN')
