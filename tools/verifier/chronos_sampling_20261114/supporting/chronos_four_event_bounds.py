#!/usr/bin/env python3
"""Exact four-event prefix bounds from the 4D Minkowski three-event census.
Python 3 stdlib only; no repo writes, network, or floating-point arithmetic.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations, product


def posets(n):
    pairs = list(combinations(range(n), 2))
    for states in product(range(3), repeat=len(pairs)):
        edges = {(a,b) for (a,b),st in zip(pairs,states) if st==1}
        edges |= {(b,a) for (a,b),st in zip(pairs,states) if st==2}
        if all((a,c) in edges for a,b in edges for bb,c in edges if bb==b):
            yield frozenset(edges)


def canonical(edges,n):
    return min(tuple(int((p[a],p[b]) in edges)
                     for a in range(n) for b in range(n) if a!=b)
               for p in permutations(range(n)))


def prefix_probability(edges,n):
    valid = [perm for perm in permutations(range(n))
             if all(perm.index(a)<perm.index(b) for a,b in edges)]
    return Q(sum((perm[0],perm[1]) in edges for perm in valid),len(valid))


def triple_type(edges):
    k=len(edges)
    if k==0: return 'A'
    if k==1: return 'E'
    if k==3: return 'C'
    assert k==2
    return 'V' if prefix_probability(edges,3)==1 else 'Lambda'


def induced(edges,sub):
    index={v:i for i,v in enumerate(sub)}
    return frozenset((index[a],index[b]) for a,b in edges if a in index and b in index)


def triple_frequencies(edges):
    counts=Counter(triple_type(induced(edges,sub))
                   for sub in combinations(range(4),3))
    return {k:Q(counts[k],4) for k in ('A','E','C','V','Lambda')}


four=list(posets(4))
assert len(four)==219
classes=defaultdict(list)
for edges in four:
    p=prefix_probability(edges,4)
    q=triple_frequencies(edges)
    lower=q['V']-q['Lambda']+q['E']/3+q['C']
    upper=Q(4,3)*q['V']+q['E']/3+Q(4,3)*q['C']
    assert lower<=p<=upper, (edges,p,lower,upper)
    classes[canonical(edges,4)].append((edges,p,q))
assert len(classes)==16
assert all(len({record[1] for record in vals})==1 for vals in classes.values())

# Exact 4D-diamond census, proved from two- and three-point causal volumes.
q3={'A':Q(53,70),'E':Q(33,175),'Lambda':Q(9,350),
    'V':Q(9,350),'C':Q(1,350)}
assert sum(q3.values())==1
lo=q3['V']-q3['Lambda']+q3['E']/3+q3['C']
hi=Q(4,3)*q3['V']+q3['E']/3+Q(4,3)*q3['C']
assert (lo,hi)==(Q(23,350),Q(53,525))

# Exact extremal convex mixtures: examples use canonical-order classes,
# and satisfy all five three-point marginals exactly.
ordered=list(classes.values())
low_support={0:Q(53,70),6:Q(33,175),11:Q(9,175),15:Q(1,350)}
high_support={0:Q(389,525),5:Q(17,525),6:Q(33,175),
              9:Q(17,525),13:Q(1,175)}
# These index sets assume itertools/product enumeration order above.
for support,target in ((low_support,lo),(high_support,hi)):
    assert sum(support.values())==1
    averaged={k:sum((weight*ordered[idx][0][2][k] for idx,weight in support.items()),Q(0))
              for k in q3}
    assert averaged==q3, (averaged,q3)
    actual=sum((weight*ordered[idx][0][1] for idx,weight in support.items()),Q(0))
    assert actual==target,(actual,target)

print('FOUR_LABELED_POSETS := 219')
print('FOUR_UNLABELED_CLASSES := 16')
print('TRIPLE_MARGINALS :=',q3)
print('LOWER_BOUND :=',lo)
print('UPPER_BOUND :=',hi)
print('INEQUALITIES_ALL_219 := PASS')
print('EXACT_EXTREMAL_MIXTURES := PASS')
print('FOUR_EVENT_MINKOWSKI_VALUE := OPEN')
print('LEAN := NOT_RUN')
