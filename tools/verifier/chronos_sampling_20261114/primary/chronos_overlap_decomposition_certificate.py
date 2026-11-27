#!/usr/bin/env python3
"""Exact finite four-poset overlap decomposition + Minkowski mixed moment.
This does NOT evaluate E[J_+^2], settle uniqueness, or verify a Lean theorem.
"""
from itertools import combinations,product
from fractions import Fraction as Q
from math import comb

def moment(r,s):
    # normalized 4D diamond null coordinates 0<=a<=b<=1, 12(b-a)^2 da db
    out=Q(0)
    for i in range(2*s+1):
        for j in range(2*s+1):
            for k,c in enumerate((1,-2,1)):
                out += Q(12*(-1)**(i+j)*comb(2*s,i)*comb(2*s,j)*c,
                         (2*r+i+k+1)*(4*r+i+j+4))
    return out
assert moment(0,0)==1
assert moment(1,0)==moment(0,1)==Q(1,20)
assert moment(2,0)==moment(0,2)==Q(1,105)
assert moment(1,2)==moment(2,1)==Q(1,35280)

pairs=list(combinations(range(4),2)); checks=0; classes={'cut':0,'bottom_comparable':0,'bottom_incomparable':0}
for states in product(range(3),repeat=6):
    edges=set()
    for (a,b),v in zip(pairs,states):
        if v==1: edges.add((a,b))
        if v==2: edges.add((b,a))
    if not all((a,c) in edges for a,b in edges for bb,c in edges if b==bb):
        continue
    cuts=[]
    for lower in pairs:
        upper=tuple(z for z in range(4) if z not in lower)
        if all((x,y) in edges for x in lower for y in upper):
            cuts.append((lower,upper))
    assert len(cuts)<=1
    cut=len(cuts)
    bottom_comp=int(bool(cut) and ((cuts[0][0][0],cuts[0][0][1]) in edges or
                                   (cuts[0][0][1],cuts[0][0][0]) in edges))
    B=int(bool(cut) and not bottom_comp)
    assert cut==B+bottom_comp
    classes['cut']+=cut
    classes['bottom_comparable']+=bottom_comp
    classes['bottom_incomparable']+=B
    checks+=1
assert checks==219
assert classes=={'cut':54,'bottom_comparable':36,'bottom_incomparable':18},classes
assert 12*moment(1,2)==Q(1,2940)
print('POSETS :=',checks)
print('CLASS_COUNTS :=',classes)
print('UNIQUE_CUT_DECOMPOSITION := PASS')
print('MINKOWSKI_MOMENTS := PASS')
print('Pr(B) = 6*E[J_plus(X,Y)^2] - 1/2940 := PROVED_IDENTITY')
print('E[J_plus(X,Y)^2] := OPEN')
print('FIXED_PREFIX_UNIQUENESS := OPEN')
print('LEAN_VERIFIED := NO')
