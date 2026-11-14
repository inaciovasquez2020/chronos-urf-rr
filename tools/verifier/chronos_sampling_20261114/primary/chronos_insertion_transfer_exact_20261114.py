#!/usr/bin/env python3
"""Exhaustive exact verification of one-point insertion/rank bias transfer.
No inference about Minkowski infinite limits; no Lean claim.
"""
from itertools import combinations,product
from fractions import Fraction as Q
from collections import Counter

def extensions(nodes, rel):
    nodes=tuple(nodes)
    pred={v:{a for a,b in rel if b==v} for v in nodes}
    out=[]
    def visit(seq,rem):
        if not rem:
            out.append(tuple(seq));return
        for v in sorted(rem):
            if not pred[v].intersection(rem): visit(seq+[v],rem-{v})
    visit([],set(nodes))
    return out

def slots(L,rel,z):
    ranks={v:i+1 for i,v in enumerate(L)}
    d=max([ranks[x] for x,y in rel if y==z]+[0])
    u=min([ranks[y] for x,y in rel if x==z]+[len(L)+1])
    return d,u,u-d

pairs=list(combinations(range(4),2))
checks=0
for states in product(range(3),repeat=6):
    rel=set()
    for (a,b),v in zip(pairs,states):
        if v==1:rel.add((a,b))
        elif v==2:rel.add((b,a))
    if any((a,c) not in rel for a,b in rel for bb,c in rel if b==bb):continue
    extfull=extensions(range(4),rel)
    for z in range(4):
        nodes=[v for v in range(4) if v!=z]
        ext=extensions(nodes,rel)
        sums=Counter(tuple(v for v in E if v!=z) for E in extfull)
        assert set(sums)==set(ext)
        available={L:slots(L,rel,z) for L in ext}
        assert all(sums[L]==available[L][2] for L in ext)
        total=sum(a for d,u,a in available.values())
        assert total==len(extfull)
        # Exact insertion and restriction probabilities for every prefix length.
        for n in range(1,5):
            cnt=sum(1 for E in extfull if E.index(z)<n)
            formula=sum(max(0,min(u,n)-d) for d,u,a in available.values())
            assert cnt==formula
            if n<=3:
                # distributional TV on full restricted extensions
                tva=Q(1,2)*sum(abs(Q(sums[L],len(extfull))-Q(1,len(ext))) for L in ext)
                mean=Q(total,len(ext))
                tvb=Q(1,2)*sum(abs(Q(a,1)/mean-1) for d,u,a in available.values())/len(ext)
                assert tva==tvb
        checks+=1
assert checks==219*4,checks
print('FOUR_LABELED_POSETS := 219')
print('DELETION_INSERTION_CASES :=',checks)
print('EXACT_SLOT_COUNTS := PASS')
print('EXACT_RESTRICTION_RADON_NIKODYM := PASS')
print('EXACT_PREFIX_INSERTION_PROBABILITIES := PASS')
print('MINKOWSKI_STABILITY_SUMMABILITY := OPEN')
print('LEAN_VERIFIED := NO')
