#!/usr/bin/env python3
"""Exact rational contraction certificate: common-N=4 CSG chain moments.
Python >=3.9, standard library only. No repo edits or downloads.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict

class IV:
    def __init__(self,lo,hi=None):
        self.lo=F(lo); self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,b):
        b=asiv(b); return IV(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self): return IV(-self.hi,-self.lo)
    def __sub__(self,b):return self+(-asiv(b))
    def __mul__(self,b):
        b=asiv(b)
        q=[v*w for v in (self.lo,self.hi) for w in (b.lo,b.hi)]
        return IV(min(q),max(q))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=asiv(b); assert b.lo*b.hi>0
        return self*IV(1/b.hi,1/b.lo)
    def __pow__(self,k):
        assert isinstance(k,int) and k>=0
        if k==0:return IV(1)
        if k%2==0 and self.lo<0<self.hi:
            return IV(0,max(self.lo**k,self.hi**k))
        return IV(min(self.lo**k,self.hi**k),max(self.lo**k,self.hi**k))
    def size(self):return max(abs(self.lo),abs(self.hi))

def asiv(v):return v if isinstance(v,IV) else IV(v)

# Sparse multivariate polynomials in x,y,z (nonnegative powers).
def pconst(c):return {(0,0,0):F(c)}
def padd(a,b):
    o=defaultdict(F,a)
    for k,v in b.items():o[k]+=v
    return {k:v for k,v in o.items() if v}
def pmul(a,b):
    o=defaultdict(F)
    for ma,ca in a.items():
        for mb,cb in b.items():o[tuple(ma[i]+mb[i] for i in range(3))]+=ca*cb
    return {k:v for k,v in o.items() if v}
def pscale(a,c):return {k:v*c for k,v in a.items() if v*c}
def pdiff(a,i):
    o={}
    for k,v in a.items():
        if k[i]:
            j=list(k);j[i]-=1;o[tuple(j)]=v*k[i]
    return o
def peval(p,v):
    total=asiv(0)
    for mon,coef in p.items():
        term=IV(coef)
        for a,n in zip(v,mon):term=term*(a**n)
        total=total+term
    return total
X={(1,0,0):F(1)};Y={(0,1,0):F(1)};Z={(0,0,1):F(1)}
ONE=pconst(1)
D=pmul(pmul(padd(ONE,X),padd(padd(ONE,pscale(X,2)),Y)),
       padd(padd(padd(ONE,pscale(X,3)),pscale(Y,3)),Z))

# Expected chain-density numerator coefficients, independently checked by
# exhaustive 40-state growth below.
N2={(3,0,0):F(26,6),(2,1,0):F(45,6),(2,0,1):F(11,6),
    (2,0,0):F(26,6),(1,2,0):F(17,6),(1,1,1):F(6,6),
    (1,1,0):F(44,6),(1,0,1):F(12,6),(1,0,0):F(6,6),
    (0,2,0):F(14,6),(0,1,1):F(5,6),(0,1,0):F(8,6),
    (0,0,1):F(3,6)}
N3={(3,0,0):F(9,4),(2,1,0):F(21,4),(2,0,1):F(6,4),
    (2,0,0):F(4,4),(1,2,0):F(10,4),(1,1,1):F(4,4),
    (1,1,0):F(9,4),(1,0,1):F(3,4),(0,2,0):F(4,4),
    (0,1,1):F(2,4)}
N4=pmul(pmul(X,padd(X,Y)),padd(padd(X,pscale(Y,2)),Z))
NUM=[N2,N3,N4]
TARGET=[F(1,10),F(1,350),F(1,29400)]

# Independent symbolic natural-label enumeration in Q[x,y,z]. Every
# coefficient, not merely one parameter evaluation, is checked.
def ideals(p):
    for a in range(1<<len(p)):
        if all((a&p[i])==p[i] for i in range(len(p)) if a>>i&1):yield a

def transitions(p,t):
    n=len(p)
    for a in ideals(p):
        w=bin(a).count("1")
        maxima=sum(1 for i in range(n) if a>>i&1 and not any((a>>j&1) and (p[j]>>i&1) for j in range(n)))
        numerator=pconst(0)
        for k in range(maxima,w+1):
            numerator=padd(numerator,pscale(t[k],F(comb(w-maxima,k-maxima))))
        yield p+(a,),numerator

def comb(n,k):
    from math import comb as c
    return c(n,k)

t=[ONE,X,Y,Z]
states={():ONE}
for stage in range(4):
    nxt={}
    for p,massnum in states.items():
        for q,w in transitions(p,t):
            nxt[q]=padd(nxt.get(q,{}),pmul(massnum,w))
    states=nxt
    assert len(states)==(1,2,7,40)[stage]
total=pconst(0)
for massnum in states.values():
    total=padd(total,massnum)
assert total==D, "CSG enumeration total mass differs from D"
for k,N in zip((2,3,4),NUM):
    numerator=pconst(0)
    for p,w in states.items():
        chains=sum(all((p[j]>>i)&1 for i,j in combinations(S,2)) for S in combinations(range(4),k))
        numerator=padd(numerator,pscale(w,F(chains,comb(4,k))))
    assert numerator==N, "CSG enumeration chain numerator differs from NUM"
print('INDEPENDENT_40_STATE_ENUMERATION := PASS')
print('EXACT_POLYNOMIAL_COEFFICIENTS := PASS')

# Exact rational Jacobian for F_i = N_i / D.
Dpartials=[pdiff(D,j) for j in range(3)]
JN=[[padd(pmul(pdiff(N,j),D),pscale(pmul(N,Dpartials[j]),-1))
     for j in range(3)] for N in NUM]
D2=pmul(D,D)
center=[F(684064,100000000),F(222049,10000000),F(17390282,100000000)]
cp=[IV(q) for q in center]
J0=[[peval(JN[i][j],cp).lo/peval(D2,cp).lo for j in range(3)] for i in range(3)]

def inverse3(a):
    rows=[row[:]+[F(int(i==j)) for j in range(3)] for i,row in enumerate(a)]
    for j in range(3):
        q=next(k for k in range(j,3) if rows[k][j])
        rows[j],rows[q]=rows[q],rows[j]
        pivot=rows[j][j];rows[j]=[x/pivot for x in rows[j]]
        for k in range(3):
            if k!=j:
                f=rows[k][j]
                rows[k]=[a-f*b for a,b in zip(rows[k],rows[j])]
    return [r[3:] for r in rows]
A=inverse3(J0)
assert all(sum(A[i][k]*J0[k][j] for k in range(3))==int(i==j) for i in range(3) for j in range(3))
res=[peval(NUM[i],cp).lo/peval(D,cp).lo-TARGET[i] for i in range(3)]
step=[sum(A[i][k]*res[k] for k in range(3)) for i in range(3)]
rad=F(1,100000)
box=[IV(c-rad,c+rad) for c in center]
assert all(v.lo>0 for v in box)
Jbox=[[peval(JN[i][j],box)/peval(D2,box) for j in range(3)]for i in range(3)]
K=[[IV(int(i==j))-sum((IV(A[i][k])*Jbox[k][j] for k in range(3)),IV(0))
    for j in range(3)]for i in range(3)]
rows=[sum(t.size() for t in rr) for rr in K]
assert max(rows)<F(1,50)
assert max(abs(v) for v in step)<rad/1000
assert max(abs(step[i])/rad+rows[i] for i in range(3))<1
print('EXACT_INTERVAL_NEWTON := PASS')
print('COUPLINGS_BOX :=',*(f'({q-rad},{q+rad})' for q in center))
print('JACOBIAN_CONTRACTION_ROW_UPPER :=',*(str(v) for v in rows))
print('ROW_BOUNDS_LT_1_OVER_50 := PASS')
print('NEWTON_CENTER_SHIFT_LT_RADIUS_OVER_1000 := PASS')
print('COMMON_FOUR_EVENT_P2 := 1/10')
print('COMMON_FOUR_EVENT_P3 := 1/350')
print('COMMON_FOUR_EVENT_P4 := 1/29400')
print('EXISTENCE_AND_LOCAL_UNIQUENESS := PROVED_BY_CONTRACTION')
print('GLOBAL_CONTINUUM_LIMIT := OPEN; LEAN := NOT_RUN; REPOSITORY := UNCHANGED')
