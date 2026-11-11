#!/usr/bin/env python3
"""Exact 5->6 causal-growth obstruction. Standard library only; no repository changes."""
from collections import defaultdict, Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, combinations

@lru_cache(None)
def canonical(rows):
    n=len(rows)
    e=[(i,j) for j in range(n) for i in range(j) if rows[j]>>i & 1]
    best=None
    for perm in permutations(range(n)):
        inv=[0]*n
        for j,i in enumerate(perm): inv[i]=j
        a=tuple(sorted((inv[i],inv[j]) for i,j in e))
        if best is None or a<best:best=a
    return best

def ideals(rows):
    n=len(rows)
    for s in range(1<<n):
        if all(not(s>>j&1) or rows[j]&s==rows[j] for j in range(n)):
            yield s

def maximal(rows):
    return [i for i in range(len(rows)) if not any(rows[j]>>i&1 for j in range(len(rows)))]

def remove_max(rows,i):
    return tuple((rows[j]&((1<<i)-1))|((rows[j]>>(i+1))<<i) for j in range(len(rows)) if j!=i)

def features(rows):
    n=len(rows)
    pair=sum(rows[j].bit_count() for j in range(n))
    triple=sum((rows[j]>>i&1) and (rows[k]>>j&1) for i,j,k in combinations(range(n),3))
    two_two=0
    for pts in combinations(range(n),4):
        edges=[(i,j) for i,j in combinations(pts,2) if rows[j]>>i&1]
        two_two+=(len(edges)==2 and len(set(sum(([i,j] for i,j in edges),[])))==4)
    return (Q(pair,15),Q(triple,20),Q(two_two,15))

def solve(B,b):
    a=[list(map(Q,row))+[Q(v)] for row,v in zip(B,b)]
    n=len(b)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:return None
        a[j],a[pivot]=a[pivot],a[j]
        v=a[j][j];a[j]=[x/v for x in a[j]]
        for i in range(n):
            if i!=j:
                f=a[i][j];a[i]=[x-f*y for x,y in zip(a[i],a[j])]
    return tuple(row[-1] for row in a)

states=[()]
for n in range(1,7):
    states=[r+(p,) for r in states for p in ideals(r)]
    print('LABELED_POSETS',n,len(states))
    if n==5:five=states[:]
    if n==6:six=states[:]
assert len(five)==357 and len(six)==4824
q={canonical((0,0,0,0,0)):Q(11,70),
   canonical((0,1,0,0,0)):Q(5,7),
   canonical((0,1,3,0,0)):Q(1,35),
   canonical((0,1,0,4,0)):Q(1,10)}
assert len(q)==4 and sum(q.values())==1
keys=sorted(q)
classes=defaultdict(list)
for r in six:
    if all(canonical(remove_max(r,i)) in q for i in maximal(r)):
        classes[canonical(r)].append(r)
assert sum(map(len,classes.values()))==132 and len(classes)==9
V=[];S=[];R=[]
for key,rr in sorted(classes.items()):
    ctr=Counter(canonical(r[:5]) for r in rr)
    V.append(tuple(Q(ctr[k],len(rr)) for k in keys))
    S.append(tuple(sum((features(r)[i] for r in rr),Q(0))/len(rr) for i in range(3)))
    R.append(rr[0])

vertices=[]
for ids in combinations(range(9),4):
    matrix=[[V[j][i] for j in ids] for i in range(4)]
    x=solve(matrix,[q[k] for k in keys])
    if x is None or min(x)<0:continue
    w=[Q(0)]*9
    for j,v in zip(ids,x):w[j]=v
    assert [sum(w[j]*V[j][i] for j in range(9)) for i in range(4)]==[q[k] for k in keys]
    vertices.append(tuple(w))
assert vertices
for k,name in enumerate(['P2','P3','P22']):
    v=[(sum(w[j]*S[j][k] for j in range(9)),w) for w in vertices]
    low=min(v,key=lambda x:x[0]);high=max(v,key=lambda x:x[0])
    print('EXACT_BOUNDS',name,low[0],high[0])
    print('MIN_WITNESS',[(j+1,z) for j,z in enumerate(low[1]) if z])
    print('MAX_WITNESS',[(j+1,z) for j,z in enumerate(high[1]) if z])
    if name=='P2':assert (low[0],high[0])==(Q(53,350),Q(2,5))
    if name=='P3':assert (low[0],high[0])==(Q(2,175),Q(9,175))
    if name=='P22':assert (low[0],high[0])==(Q(1,150),Q(1,50))

# Exact dual lower certificates, coordinates in canonical sorted five-class order.
dual_pair={canonical((0,0,0,0,0)):Q(-3,5),canonical((0,1,0,0,0)):Q(2,5),canonical((0,1,3,0,0)):Q(0),canonical((0,1,0,4,0)):Q(-2,5)}
dual_three={canonical((0,0,0,0,0)):Q(-1,10),canonical((0,1,0,0,0)):Q(1,20),canonical((0,1,3,0,0)):Q(1,20),canonical((0,1,0,4,0)):Q(-1,10)}
for name,k,d,expected in [('P2',0,dual_pair,Q(53,350)),('P3',1,dual_three,Q(2,175))]:
    assert sum(d[c]*q[c] for c in keys)==expected
    gaps=[S[j][k]-sum(d[c]*V[j][i] for i,c in enumerate(keys)) for j in range(9)]
    assert min(gaps)>=0
    print('DUAL_CERTIFICATE',name,'BOUND',expected,'SLACKS',gaps)
print('RESULT := COMPUTATION_PASS_EXACT')
print('MINKOWSKI_PAIR',Q(1,10),'MINKOWSKI_THREE',Q(1,350))
print('FINITE_EXTENSION_MATCH_N5_AND_N6 := IMPOSSIBLE')