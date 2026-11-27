from fractions import Fraction as F
from math import factorial
from itertools import combinations, permutations
# Independently enumerate natural triples, using orbit canonicalization.
E=list(combinations(range(3),2)); classes={}
for mask in range(8):
    r=frozenset(e for k,e in enumerate(E) if (mask>>k)&1)
    if (0,1) in r and (1,2) in r and (0,2) not in r: continue
    key=min(tuple(sorted((p[i],p[j]) for i,j in r)) for p in permutations(range(3)))
    classes.setdefault(key,[]).append(r)
assert sorted(map(len,classes.values()))==[1,1,1,1,3]
def kind(r):
    return {0:'A',1:'E',3:'C'}.get(len(r),'V' if len({i for i,j in r})==1 else 'W')
weights={kind(rs[0]):F(sum((0,1) in r for r in rs),len(rs)) for rs in classes.values()}
# Exact all-dimension moments: integral of u^k (1-u)^(d-2).
# For integer d>=2 and integer s>=0, k=d*s/2 is rational and
# the beta factor equals (d-2)!/product(k+j,j=1..d-1).
def moment(d,s):
    k=F(d*s,2); b=F(factorial(d-2))
    for j in range(1,d): b/=k+j
    return F(d-1,s+1)*b
for d in range(2,101):
    p=2*moment(d,1); m=moment(d,2); c=3*m*p; f=3*m*(1-p)
    e=3*p-3*c-4*f; a=1-e-c-2*f
    q=dict(A=a,E=e,V=f,W=f,C=c)
    assert min(q.values())>=0 and sum(q.values())==1
    prefix=sum(q[k]*weights[k] for k in q)
    assert p-prefix==f/3==m*(1-p)>0
    if d in (2,3,4,5,6,10): print(f'd={d}: p={p} delta={p-prefix}')
# All exchangeable triple distributions need not be time reversal symmetric.
# Check the universal discrepancy formula on a rational simplex grid.
checks=0
for a in range(21):
 for e in range(21-a):
  for v in range(21-a-e):
   for w in range(21-a-e-v):
    c=20-a-e-v-w
    q=dict(A=F(a,20),E=F(e,20),V=F(v,20),W=F(w,20),C=F(c,20))
    pair=(q['E']+2*q['V']+2*q['W']+3*q['C'])/3
    prefix=sum(q[k]*weights[k] for k in q)
    assert pair-prefix==(2*q['W']-q['V'])/3
    checks+=1
print('DIMENSIONS_CHECKED := 99')
print('GENERAL_SIMPLEX_CASES :=',checks)
print('COMPUTATION_PASS; LEAN_NOT_RUN; NOVELTY_NOT_ESTABLISHED')
