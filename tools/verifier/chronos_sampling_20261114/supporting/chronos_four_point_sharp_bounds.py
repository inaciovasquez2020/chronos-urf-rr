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



# Four-point geometry: W is the conditional fraction of the diamond in a point's past.
# E[W^k] = 12/((2k+1)(2k+3)) - 3/(k+1)^2.
assert Q(12,7*9)-Q(3,16)==Q(1,336)
top_probability=bottom_probability=Q(4,336)  # unique greatest/least among four points

def greatest(e):
    return int(any(all((b,a) in e for b in range(4) if b!=a) for a in range(4)))
def least(e):
    return int(any(all((a,b) in e for b in range(4) if b!=a) for a in range(4)))

four=list(posets(4))
assert len(four)==219
classes={}
for e in four:
    p=prefix_probability(e,4); q=triple_frequencies(e)
    t=greatest(e); b=least(e)
    lower=q['E']/3-q['C']/3+2*q['V']/3-2*q['Lambda']/3+Q(t+b,2)
    upper=q['E']/3+q['C']+4*q['V']/3-2*q['Lambda']/3+Q(t,2)
    assert lower<=p<=upper, (e,p,lower,upper)
    key=canonical(e,4)
    assert key not in classes or classes[key][1:]==(p,q,t,b)
    classes[key]=(e,p,q,t,b)
assert len(classes)==16
q3={'A':Q(53,70),'E':Q(33,175),'Lambda':Q(9,350),
    'V':Q(9,350),'C':Q(1,350)}
assert sum(q3.values())==1
lo=q3['E']/3-q3['C']/3+2*q3['V']/3-2*q3['Lambda']/3+(top_probability+bottom_probability)/2
hi=q3['E']/3+q3['C']+4*q3['V']/3-2*q3['Lambda']/3+top_probability/2
assert (lo,hi)==(Q(31,420),Q(373,4200))

# Exact primal rational witnesses for each endpoint, independent of floating point LP.
ordered=list(classes.values())
low_support={0:Q(631,840),2:Q(1,175),5:Q(13,2100),6:Q(13,70),9:Q(1,84),11:Q(47,1400),12:Q(1,175)}
high_support={0:Q(1507,2100),2:Q(47,700),3:Q(11,140),5:Q(1,84),6:Q(79,700),9:Q(1,2100),10:Q(2,175)}
for support,target in ((low_support,lo),(high_support,hi)):
    assert sum(support.values())==1
    assert all(sum((weight*ordered[i][2][k] for i,weight in support.items()),Q(0))==q3[k] for k in q3)
    assert sum((weight*ordered[i][3] for i,weight in support.items()),Q(0))==top_probability
    assert sum((weight*ordered[i][4] for i,weight in support.items()),Q(0))==bottom_probability
    assert sum((weight*ordered[i][1] for i,weight in support.items()),Q(0))==target


# Time-reversal symmetry holds for the Minkowski diamond.
for e in four:
    rev=frozenset((b,a) for a,b in e)
    psym=(prefix_probability(e,4)+prefix_probability(rev,4))/2
    q=triple_frequencies(e)
    t=greatest(e); b=least(e)
    low_sym=q['E']/3+Q(t+b,2)
    high_sym=q['E']/3+q['C']+(q['V']+q['Lambda'])/3+Q(t+b,4)
    assert low_sym<=psym<=high_sym
sym_lo=q3['E']/3+(top_probability+bottom_probability)/2
sym_hi=q3['E']/3+q3['C']+(q3['V']+q3['Lambda'])/3+(top_probability+bottom_probability)/4
assert (sym_lo,sym_hi)==(Q(157,2100),Q(373,4200))

# Attaining symmetry-respecting distributions (canonical class indices).
sym_low={0:Q(3161,4200),5:Q(19,2100),6:Q(33,175),9:Q(19,2100),11:Q(7,200),12:Q(1,350),14:Q(1,350)}
sym_high={0:Q(1507,2100),2:Q(47,700),3:Q(47,700),4:Q(2,175),5:Q(1,84),6:Q(79,700),9:Q(1,84)}
for support,target in ((sym_low,sym_lo),(sym_high,sym_hi)):
    assert sum(support.values())==1
    assert all(sum((weight*ordered[i][2][k] for i,weight in support.items()),Q(0))==q3[k] for k in q3)
    assert sum((weight*ordered[i][3] for i,weight in support.items()),Q(0))==top_probability
    assert sum((weight*ordered[i][4] for i,weight in support.items()),Q(0))==bottom_probability
    assert sum((weight*ordered[i][1] for i,weight in support.items()),Q(0))==target
    for i,weight in support.items():
        rev=frozenset((b,a) for a,b in ordered[i][0])
        j=next(k for k,v in enumerate(ordered) if canonical(v[0],4)==canonical(rev,4))
        assert support.get(j,Q(0))==weight

print('STATUS := COMPUTATION_PASS')
print('FOUR_LABELED_POSETS :=',len(four))
print('UNLABELED_CLASSES :=',len(classes))
print('FOUR_POINT_MOMENT := 1/336')
print('GREATEST_AND_LEAST_PROBABILITY := 1/84 EACH')
print('LOWER :=',lo,'UPPER :=',hi)
print('TIME_REVERSAL_SHARP_LOWER :=',sym_lo,'TIME_REVERSAL_SHARP_UPPER :=',sym_hi)
print('DUAL_BOUNDS := VERIFIED_ALL_POSETS')
print('PRIMAL_EXTREMIZERS := VERIFIED_EXACT_RATIONAL')
print('INTERVAL_OPTIMALITY := ONLY_GIVEN_LISTED_MARGINALS')
print('ACTUAL_P_4_2 := OPEN')
print('LEAN := NOT_RUN')
