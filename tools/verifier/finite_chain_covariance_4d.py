"""Exact rational 4D causal-diamond chain covariance, fixed N.

Bounded evidence: one-point polynomial moments, finite-N pair entries,
generic overlap coefficients via independent exhaustive discrete oracle.
The shared-two 3-chain integral gamma2 remains OPEN.
"""
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations, product
from math import factorial, comb

if not __debug__:
    raise SystemExit("INCOMPLETE: Python assertions disabled")

def add(*ps):
    ans = defaultdict(F)
    for p in ps:
        for k, v in p.items():
            ans[k] += v
    return {k: v for k, v in ans.items() if v}

def mul(a, b):
    ans = defaultdict(F)
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            ans[(i+k, j+l)] += v*w
    return {k: v for k, v in ans.items() if v}

def scale(p, c):
    return {k: c*v for k, v in p.items() if c*v}

def powpoly(p, n):
    v = {(0,0): F(1)}
    for _ in range(n):
        v = mul(v,p)
    return v

one = {(0,0):F(1)}
t = {(1,0):F(1)}
r2 = {(0,2):F(1)}
A = powpoly(add(one, scale(t,2), powpoly(t,2), scale(r2,-1)),2)
B = powpoly(add(one, scale(t,-2), powpoly(t,2), scale(r2,-1)),2)
h = scale(add(A,B),F(1,16))
q = scale(add(mul(A,B),scale(add(powpoly(A,2),powpoly(B,2)),F(1,20))),F(1,128))

def E(p):
    v=F(0)
    for (i,j),coeff in p.items():
        assert i%2 == 0 and j%2 == 0
        v += coeff * F(12*factorial(i)*factorial(j+2), factorial(i+j+4))
    return v

p2,p3=F(1,10),F(1,350)
assert (E(h),E(mul(h,h)),E(q),E(mul(h,q)),E(mul(q,q))) == (
    p2,F(1,50),p3,F(1,1400),F(29,970200))
vh=E(mul(h,h))-p2*p2
cq=E(mul(h,q))-p2*p3
vq=E(mul(q,q))-p3*p3
assert (vh,cq,vq)==(F(1,100),F(3,7000),F(527,24255000))

sigma=((4*vh,6*cq),(6*cq,9*vq))
assert sigma==((F(1,25),F(9,3500)),(F(9,3500),F(527,2695000)))
J11,J21,J22=F(1,25),F(9,3500),F(16,165375)
assert J11*J22==F(16,4134375)
inv11,inv21,inv22=1/J11,-J21/(J11*J22),1/J22
assert (inv11**2*sigma[0][0],
        inv11*(inv21*sigma[0][0]+inv22*sigma[0][1]),
        inv21**2*sigma[0][0]+2*inv21*inv22*sigma[0][1]+inv22**2*sigma[1][1]
       )==(F(25),F(0),F(145563075,45056))

def C(n,k):
    return comb(n,k) if 0<=k<=n else 0

for N in range(3,18):
    v22 = F(2*(N-2),C(N,2))*vh + F(1,C(N,2))*p2*(1-p2)
    v23 = F(2*C(N-2,2),C(N,3))*cq + F(N-2,C(N,3))*(p3-p2*p3)
    assert v22==F(2*N+5,50*N*(N-1))
    assert v23==F(9*(N+3),3500*N*(N-1))

# Independent exact finite oracle for generic overlap coefficients.
# Sample iid with replacement from a three-atom chain (not Minkowski).
def pair(a,b): return int(a!=b)
def triple(a,b,c): return int(len({a,b,c})==3)
def av(k,fun):
    xs=list(product(range(3),repeat=k))
    return F(sum(fun(x) for x in xs),len(xs))

pd=av(2,lambda x:pair(*x))
td=av(3,lambda x:triple(*x))
vd=av(3,lambda x:pair(x[0],x[1])*pair(x[0],x[2]))-pd**2
cd=av(4,lambda x:pair(x[0],x[1])*triple(x[0],x[2],x[3]))-pd*td
wd=av(5,lambda x:triple(*x[:3])*triple(x[0],x[3],x[4]))-td**2
gamma=av(4,lambda x:triple(*x[:3])*triple(x[0],x[1],x[3]))
for N in (3,4,5):
    allrows=list(product(range(3),repeat=N))
    u2=lambda row:F(sum(pair(row[i],row[j]) for i,j in combinations(range(N),2)),C(N,2))
    u3=lambda row:F(sum(triple(row[i],row[j],row[k]) for i,j,k in combinations(range(N),3)),C(N,3))
    a2=[u2(row) for row in allrows]
    a3=[u3(row) for row in allrows]
    cv22=F(sum(v*v for v in a2),len(a2))-pd**2
    cv23=F(sum(x*y for x,y in zip(a2,a3)),len(a2))-pd*td
    cv33=F(sum(v*v for v in a3),len(a3))-td**2
    pred22=F(2*(N-2),C(N,2))*vd+F(1,C(N,2))*pd*(1-pd)
    pred23=F(2*C(N-2,2),C(N,3))*cd+F(N-2,C(N,3))*(td-pd*td)
    pred33=(F(3*C(N-3,2),C(N,3))*wd+
            F(3*(N-3),C(N,3))*(gamma-td**2)+
            F(1,C(N,3))*td*(1-td))
    assert (cv22,cv23,cv33)==(pred22,pred23,pred33)

print("MONOMIAL_MOMENT_AUDIT := PASS")
print("FINITE_N_OVERLAP_ORACLE := PASS")
print("LEADING_SIGMA :=",sigma)
print("LEADING_PARAMETER_VARIANCES := 25, 145563075/45056")
print("GAMMA2_EXACT_4D_INTEGRAL := OPEN")
print("RESULT := COMPUTATION_PASS")
