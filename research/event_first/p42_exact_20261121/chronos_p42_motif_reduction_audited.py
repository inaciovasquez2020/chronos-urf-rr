#!/usr/bin/env python3
"""Exact finite-poset linear identity reducing Chronos p_(4,2) to four motifs.

Scope: combinatorial identity conditional on exact 3-event frequencies, four-event
extrema, time-reversal and two specified four-event geometric statistics.
Does not evaluate the four remaining motif probabilities.
Python stdlib only.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import Counter


def posets(n):
    for sts in product(range(3), repeat=n*(n-1)//2):
        e = set()
        for (a,b),st in zip(combinations(range(n),2),sts):
            if st: e.add((a,b) if st==1 else (b,a))
        if all((a,c) in e for a,b in e for bb,c in e if bb==b):
            yield frozenset(e)


def key(e,n):
    return min(tuple(int((p[a],p[b]) in e) for a in range(n)
                     for b in range(n) if a != b) for p in permutations(range(n)))


def prefix(e,n):
    perms=[p for p in permutations(range(n)) if all(p.index(a)<p.index(b) for a,b in e)]
    return F(sum((p[0],p[1]) in e for p in perms),len(perms))


def typ(e):
    k=len(e)
    if k==0:return 'A'
    if k==1:return 'E'
    if k==3:return 'C'
    return 'V' if prefix(e,3)==1 else 'Lambda'


def freq(e):
    c=Counter()
    for sub in combinations(range(4),3):
        ind={v:i for i,v in enumerate(sub)}
        c[typ(frozenset((ind[a],ind[b]) for a,b in e if a in ind and b in ind))]+=1
    return {k:F(c[k],4) for k in ('A','E','V','Lambda','C')}


def greatest(e):return int(any(all((b,a) in e for b in range(4) if a!=b) for a in range(4)))
def least(e):return int(any(all((a,b) in e for b in range(4) if a!=b) for a in range(4)))
def central(e):return int(any(sum((a,x) in e for a in range(4) if a!=x)==2 and sum((x,b) in e for b in range(4) if b!=x)==1 for x in range(4)))

labeled=list(posets(4))
classes={}
for e in labeled: classes.setdefault(key(e,4),e)
assert len(labeled)==219 and len(classes)==16
ordered=list(classes.values())
rev=[]
for i,e in enumerate(ordered):
    rr=frozenset((b,a) for a,b in e)
    rev.append(next(j for j,f in enumerate(ordered) if key(f,4)==key(rr,4)))
assert [(i,j) for i,j in enumerate(rev) if i<j]==[(2,3),(5,9),(8,10),(12,14)]
# exact certificate: 14 rows = normalization; q3 A/E/V/Lambda/C;
# greatest/least; four reversal constraints; center; four-chain.
rows=[[F(1)]*16]
for k in ('A','E','V','Lambda','C'):rows.append([freq(e)[k] for e in ordered])
rows += [[F(greatest(e)) for e in ordered], [F(least(e)) for e in ordered]]
for i,j in enumerate(rev):
    if i<j: rows.append([F(int(k==i)-int(k==j)) for k in range(16)])
rows += [[F(central(e)) for e in ordered], [F(int(len(e)==6)) for e in ordered]]
assert len(rows)==14
coeff=[F(0),F(0),F(1,3),F(2),F(-4,3),F(1),F(1),F(-1,2),F(1,6),F(0),F(-1,6),F(0),F(-5,6),F(1,3)]
residual={7:F(-2,15),8:F(-1,6),11:F(-1,3),13:F(-1,6)}
for i,e in enumerate(ordered):
    claimed=sum((y*row[i] for y,row in zip(coeff,rows)),F(0))+residual.get(i,F(0))
    assert claimed==prefix(e,4),(i,e,claimed,prefix(e,4))
known=[F(1),F(53,70),F(33,175),F(9,350),F(9,350),F(1,350),F(1,84),F(1,84), F(0),F(0),F(0),F(0),F(1,2940),F(1,29400)]
constant=sum((y*b for y,b in zip(coeff,known)),F(0))
assert constant==F(2603,29400)
# Canonical-isomorphism guards: labels of representatives are arbitrary.
# These four representatives are produced by the same deterministic class order
# used by the exact rational identity and its source certificate.
expected_reps = {
    7: [(0,3),(1,2),(1,3)],
    8: [(0,3),(1,2),(1,3),(2,3)],
    11: [(0,2),(0,3),(1,2),(1,3)],
    13: [(0,2),(1,2),(3,0),(3,1),(3,2)],
}
assert all(key(ordered[i],4)==key(frozenset(rep),4)
           for i,rep in expected_reps.items())
assert len({key(ordered[i],4) for i in expected_reps})==4
# Two exact nonnegative distributions agree on all fourteen supplied
# moment/symmetry constraints but have distinct p_(4,2). This proves
# those constraints alone do not identify the actual Minkowski value.
low_witness = {
    0:F(277,490), 1:F(66,175), 5:F(8,1225), 9:F(8,1225),
    11:F(163,4200), 12:F(3,9800), 13:F(37,7350),
    14:F(3,9800), 15:F(1,29400),
}
high_witness = {
    0:F(17761,29400), 1:F(278,1225), 2:F(331,4900),
    3:F(331,4900), 4:F(37,3675), 5:F(17,1470),
    9:F(17,1470), 12:F(3,9800), 14:F(3,9800),
    15:F(1,29400),
}
for witness, endpoint in ((low_witness,F(157,2100)),
                          (high_witness,F(2603,29400))):
    assert all(q >= 0 for q in witness.values())
    assert sum(witness.values()) == 1
    for row, required in zip(rows, known):
        assert sum((witness.get(i,F(0))*row[i] for i in range(16)),F(0)) == required
    assert sum((witness.get(i,F(0))*prefix(e,4)
                for i,e in enumerate(ordered)),F(0)) == endpoint
assert F(157,2100) != F(2603,29400)
print('CONSTRAINT_NONIDENTIFIABILITY := PASS (two exact rational witnesses)')
print('CONSTRAINT_ONLY_BOUNDS := 157/2100 <= p_4_2 <= 2603/29400')
print('FOUR_LABELED_POSETS :=',len(labeled))
print('FOUR_UNLABELED_CLASSES :=',len(classes))
print('PER_CLASS_RATIONAL_IDENTITY := PASS (16/16)')
print('KNOWN_CONSTRAINT_CONSTANT :=',constant)
print('P_4_2 = 2603/29400 - 2*q7/15 - q8/6 - q11/3 - q13/6')
print('EXACT_P_4_2 := OPEN (four motif probabilities not integrated)')
print('LEAN := NOT_RUN')
