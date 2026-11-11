#!/usr/bin/env python3
"""Exact infinite-extension certificate for a finite five-event causal-order law.
No network, packages or repository mutation. All probabilities are rational.
"""
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter
from math import comb

N0=5
pairs=list(combinations(range(N0),2))
def closure(mask):
    rows=[0]*N0
    for k,(i,j) in enumerate(pairs):
        if mask>>k&1: rows[i]|=1<<j
    for k in range(N0):
        for i in range(k):
            if rows[i]>>k&1:rows[i]|=rows[k]
    return tuple(rows)
def signature(r):
    edge=sum(z.bit_count() for z in r)
    chain=sum(bool(r[i]>>j&1 and r[j]>>k&1) for i,j,k in combinations(range(5),3))
    two=0
    for v in combinations(range(5),4):
        edges=[(i,j) for i,j in combinations(v,2) if r[i]>>j&1]
        if len(edges)==2 and len(set(edges[0]+edges[1]))==4:two+=1
    return edge,chain,two
labels={(0,0,0):'empty',(1,0,0):'edge',(3,1,0):'chain3',(2,0,1):'two_plus_two'}
class_mass={'empty':Q(11,70),'edge':Q(5,7),'chain3':Q(1,35),'two_plus_two':Q(1,10)}
orders={closure(i) for i in range(2**len(pairs))}
counts=Counter(labels.get(signature(r)) for r in orders)
assert counts==Counter({None:321,'empty':1,'edge':10,'chain3':10,'two_plus_two':15})
terminal={r:(class_mass[labels[signature(r)]]/counts[labels[signature(r)]] if signature(r) in labels else Q(0)) for r in orders}
assert sum(terminal.values())==1

def cone(r):
    n=len(r)
    return tuple(z|(1<<n) for z in r)+(0,)
def pref(r,n):return tuple(z&((1<<n)-1) for z in r[:n])
def swap_last(r):
    n=len(r);a=n-2;b=n-1
    def sw(i):return b if i==a else a if i==b else i
    return tuple(sum(1<<sw(j) for j in range(n) if r[sw(i)]>>j&1) for i in range(n))

def measure(n):
    """Unique history distribution: prefixes to 5; subsequent all-past cone extensions."""
    out=Counter()
    for r,p in terminal.items():
        if p==0:continue
        if n<=5:out[pref(r,n)]+=p
        else:
            s=r
            for _ in range(n-5):s=cone(s)
            out[s]+=p
    return out

# Check all possible transitions have normalized total, and all reachable incomparable squares commute.
all_squares=0
for n in range(0,10):
    A=measure(n); B=measure(n+1)
    assert sum(A.values())==1 and sum(B.values())==1
    for r,pr in A.items():
        assert sum(w for s,w in B.items() if pref(s,n)==r)==pr
    if n>=1:
        for s,w in B.items():
            if not(s[n-1]>>n&1):  # no relation between last two positions
                assert B[swap_last(s)]==w,(n,s,w)
                all_squares+=1

paircount=sum(p*signature(r)[0] for r,p in terminal.items())
triplecount=sum(p*signature(r)[1] for r,p in terminal.items())
twotwocount=sum(p*signature(r)[2] for r,p in terminal.items())
assert (paircount,triplecount,twotwocount)==(Q(1),Q(1,35),Q(1,10))

def exact_moments(n):
    m=n-5
    pairs_mean=(comb(n,2)-Q(9))/comb(n,2)
    triples_mean=(comb(m,3) if m>=3 else 0)+(5*comb(m,2) if m>=2 else 0)+m*paircount+triplecount
    triple_density=Q(triples_mean,comb(n,3))
    two_density=twotwocount/Q(comb(n,4))
    return pairs_mean,triple_density,two_density

for n in range(5,11):
    A=measure(n)
    p2=sum(p*Q(sum(z.bit_count() for z in r),comb(n,2)) for r,p in A.items())
    p3=sum(p*Q(sum(bool(r[i]>>j&1 and r[j]>>k&1) for i,j,k in combinations(range(n),3)),comb(n,3)) for r,p in A.items())
    two=0
    for r,p in A.items():
        c=0
        for v in combinations(range(n),4):
            edges=[(i,j) for i,j in combinations(v,2) if r[i]>>j&1]
            if len(edges)==2 and len(set(edges[0]+edges[1]))==4:c+=1
        two+=p*Q(c,comb(n,4))
    assert (p2,p3,two)==exact_moments(n), (n,(p2,p3,two),exact_moments(n))

print('SOURCE_FIVE_SUPPORT := 36')
print('FIVE_MOMENTS := P2 1/10, P3 1/350, U2PLUS2 1/50')
print('EXACT_EXTENSION := cone over all past events after fifth birth')
print('PROJECTIVITY_AND_COVARIANCE_TESTED_LEVELS := 0..10')
print('ADJACENT_SWAP_CASES :=',all_squares)
for n in (5,6,10,20,100):print('N',n,'P2_P3_2PLUS2',*(str(x) for x in exact_moments(n)))
print('P2_LIMIT := 1')
print('P3_LIMIT := 1')
print('U2PLUS2_LIMIT := 0')
print('RESULT := COMPUTATION_PASS; infinite theorem analytical')