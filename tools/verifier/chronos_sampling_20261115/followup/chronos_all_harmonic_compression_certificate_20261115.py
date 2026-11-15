#!/usr/bin/env python3
"""Exact all-angular-modes finite rank lower certificates for 4D Minkowski.

Preconditions: spherical harmonic decomposition and exact p42 four-point reduction.
The finite-dimensional compression uses the exact Lorentz-equivariant action on
solid spherical harmonics. Only Python standard library rational arithmetic.
"""
from fractions import Fraction as Q
from math import factorial, comb

def beta(a,b):
    return Q(factorial(a-1)*factorial(b-1),factorial(a+b-1))

def kappa(ell,m):
    # E[(t+r cos(theta))^ell * W_-^m], uniform cos(theta) on [-1,1]
    return Q(12,(ell+1)*(4*m+ell+4)) * (
        Q(1,2*m+1)-Q(1,2*m+2)-Q(1,2*m+ell+2)+Q(1,2*m+ell+3))

def G(ell,k):
    # E[r^(2ell)*W_-^k]
    return Q(12,4**ell*(4*k+2*ell+4))*beta(2*k+1,2*ell+3)

def inverse(A):
    n=len(A)
    R=[[A[i][j] for j in range(n)]+[Q(int(i==j)) for j in range(n)] for i in range(n)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if R[i][j]),None)
        assert pivot is not None,'singular Gram'
        R[j],R[pivot]=R[pivot],R[j]
        z=R[j][j]
        R[j]=[v/z for v in R[j]]
        for i in range(n):
            if i!=j:
                z=R[i][j]
                R[i]=[u-z*v for u,v in zip(R[i],R[j])]
    return [row[n:] for row in R]

def mul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Q()) for j in range(len(B[0]))]
            for i in range(len(A))]

def trace(A): return sum((A[i][i] for i in range(len(A))),Q())

def compression(ell,d):
    gram=[[G(ell,i+j) for j in range(d)] for i in range(d)]
    energy=[[kappa(ell,i)*kappa(ell,j)*G(ell,i+j+2) for j in range(d)] for i in range(d)]
    mat=mul(inverse(gram),energy)
    return (2*ell+1)*trace(mul(mat,mat))

# Independent moment crosschecks for l=1, and l=0/l=2 trivial moments
assert kappa(0,0)==1
assert kappa(1,0)==Q(1,2)
assert G(1,0)==Q(1,10)
assert G(1,2)==Q(1,2940)
assert compression(1,1)==Q(1,460992)
assert kappa(2,0)==Q(3,10) # E[t^2]+E[r^2]/3

def independent_kappa(ell,m):
    """Independent expansion in t,r,then a,b; integrate monomials on 0<a<b<1."""
    z=Q()
    for j in range(0,ell//2+1):
        p=ell-2*j
        v=Q()
        # (a+b)^p (b-a)^(2j+2) / 2^ell
        for h in range(p+1):
            for k in range(2*j+3):
                A=2*m+h+k
                B=2*m+p-h+2*j+2-k
                v += Q(comb(p,h)*comb(2*j+2,k)*(-1)**k,(A+1)*(A+B+2))
        z += Q(12*comb(ell,2*j),(2*j+1)*2**ell)*v
    return z

for ell in range(0,10):
    for m in range(0,5):
        assert independent_kappa(ell,m)==kappa(ell,m),(ell,m)
print('INDEPENDENT_NULL_POLYNOMIAL_MOMENTS := 50/50 PASS')

A0=Q(513,875875)
base=Q(3557,42000)+Q(6,5)*A0
print('ZERO_MODE_BASELINE :=',float(base))
prev_total=Q()
for d in (1,2,3,4,5,6):
    contributions=[]
    for ell in range(1,9):
        v=compression(ell,d)
        assert v>=0
        contributions.append(v)
    total=sum(contributions,Q())
    assert total>prev_total
    prev_total=total
    bound=base+Q(6,5)*total
    print('d',d,'l1..8 lower total',format(float(total),'.15g'),'p42 >',format(float(bound),'.15g'))
    if d in (4,6):
        print('  individual angular lower:',[(ell,format(float(v),'.9g')) for ell,v in enumerate(contributions,1)])
    if d==6:
        print('CERTIFIED_EXACT_FRACTION_SHA256 :=',__import__('hashlib').sha256(str(bound).encode()).hexdigest())
        for digits in (8,9,10,11,12):
            lower=Q(int(bound*10**digits),10**digits)
            assert lower<bound
            print('CERTIFIED_DECIMAL_LOWER_'+str(digits)+' :=',format(float(lower),f'.{digits}f'))
print('EXACT_FULL_TRACE := OPEN')
print('RESULT := COMPUTATION_PASS')
