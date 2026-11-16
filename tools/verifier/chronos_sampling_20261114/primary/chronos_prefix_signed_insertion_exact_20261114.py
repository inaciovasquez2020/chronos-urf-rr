#!/usr/bin/env python3
"""Exact signed single-event insertion identity for prefix comparability.
Enumerates all 219 labeled four-posets and every deleted vertex; independent
full-extension enumeration vs signed covariance/slot formula. Stdlib only.
"""
from itertools import combinations,product
from fractions import Fraction as Q

def extensions(nodes,rel):
    nodes=tuple(nodes)
    pred={v:{a for a,b in rel if b==v} for v in nodes}
    out=[]
    def visit(seq,rem):
        if not rem:out.append(tuple(seq));return
        for v in sorted(rem):
            if not pred[v].intersection(rem):visit(seq+[v],rem-{v})
    visit([],set(nodes));return out

def comparable(a,b,rel):return (a,b) in rel or (b,a) in rel

def prefix_stat(L,n,rel):
    return Q(sum(comparable(a,b,rel) for a,b in combinations(L[:n],2)),n*(n-1)//2)

pairs=list(combinations(range(4),2)); checks=0
for states in product(range(3),repeat=6):
    rel=set()
    for (a,b),v in zip(pairs,states):
        if v==1:rel.add((a,b))
        elif v==2:rel.add((b,a))
    if any((a,c) not in rel for a,b in rel for bb,c in rel if b==bb):continue
    full=extensions(range(4),rel)
    for z in range(4):
        ext=extensions([v for v in range(4) if v!=z],rel)
        vals=[]
        for L in ext:
            rank={v:i+1 for i,v in enumerate(L)}
            d=max([rank[a] for a,b in rel if b==z]+[0]);u=min([rank[b] for a,b in rel if a==z]+[4]);a=u-d
            vals.append((L,a,d,u))
        e=Q(len(ext));bar_a=Q(sum(a for L,a,d,u in vals),len(ext))
        for n in (2,3):
            h=[prefix_stat(L,n,rel) for L,a,d,u in vals]
            Eh=sum(h,Q(0))/e
            EaH=sum((a*hh for (L,a,d,u),hh in zip(vals,h)),Q(0))/e
            covariance=EaH-bar_a*Eh
            correction=Q(0)
            for L,a,d,u in vals:
                m=max(0,min(u,n)-d)
                nz=sum(comparable(z,v,rel) for v in L[:n-1])
                nl=sum(comparable(L[n-1],v,rel) for v in L[:n-1])
                correction+=Q(m*(nz-nl),n*(n-1)//2)
            correction/=e
            predicted=Eh+covariance/bar_a+correction/bar_a
            actual=sum((prefix_stat(E,n,rel) for E in full),Q(0))/len(full)
            assert predicted==actual,(z,n,predicted,actual)
            checks+=1
assert checks==219*4*2
print('FOUR_POSETS := 219')
print('DELETION_CASES := 876')
print('PREFIX_CASES :=',checks)
print('SIGNED_INSERTION_IDENTITY := PASS')
print('MINKOWSKI_BIAS_ESTIMATE := OPEN')
print('LEAN_VERIFIED := NO')
