#!/usr/bin/env python3
"""Exact-rational two-sided p_(4,2) bounds using angular compression.
Conditional on the previously archived identity p42=3557/42000+6/5*sum_l A_l,
A0=513/875875 and angular HS masses b_l for l=1..5.
No floating arithmetic enters the proofs. Python standard library only.
"""
from fractions import Fraction as F
from math import factorial
import hashlib

def beta(a,b): return F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
def kappa(l,m):
    return F(12,(l+1)*(4*m+l+4))*(F(1,2*m+1)-F(1,2*m+2)-F(1,2*m+l+2)+F(1,2*m+l+3))
def moment(l,k): return F(12,4**l*(4*k+2*l+4))*beta(2*k+1,2*l+3)
def inverse(A):
    n=len(A); R=[[A[i][j] for j in range(n)]+[F(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        p=next((i for i in range(j,n) if R[i][j]),None)
        if p is None: raise ValueError('Singular Gram')
        R[j],R[p]=R[p],R[j]; z=R[j][j];R[j]=[x/z for x in R[j]]
        for i in range(n):
            if i!=j:
                z=R[i][j];R[i]=[x-z*y for x,y in zip(R[i],R[j])]
    return [r[n:] for r in R]
def mul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F()) for j in range(len(B[0]))] for i in range(len(A))]
def trace(A): return sum((row[i] for i,row in enumerate(A)),F())
def compression(l,d):
    G=[[moment(l,i+j) for j in range(d)] for i in range(d)]
    B=[[kappa(l,i)*kappa(l,j)*moment(l,i+j+2) for j in range(d)] for i in range(d)]
    V=mul(inverse(G),B)
    t=trace(V);s=trace(mul(V,V))
    assert t>0 and s>0 and t*t>=s
    return t,s

def arctan_interval(q,n=40):
    partial=sum((F((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(n)),F())
    term=F((-1)**n,(2*n+1)*q**(2*n+1))
    return min(partial,partial+term),max(partial,partial+term)
a,b=arctan_interval(5);c,d=arctan_interval(239)
pi_lo=16*a-4*d;pi_hi=16*b-4*c
assert 3<pi_lo<pi_hi<F(22,7)
coeffs=[(F(-829,14),6),(F(-35649,14),258),(F(-32925),3336),
        (F(-8083206,35),23400),(F(-155653531,140),112650)]
bounds=[(r+c*pi_lo**2,r+c*pi_hi**2) for r,c in coeffs]
assert all(0<lo<=hi for lo,hi in bounds)
R_lo=F(3,140)-sum(((2*l+1)*hi for l,(lo,hi) in enumerate(bounds,1)),F())
R_hi=F(3,140)-sum(((2*l+1)*lo for l,(lo,hi) in enumerate(bounds,1)),F())
assert 0<R_lo<R_hi
base=F(3557,42000);A0=F(513,875875)
previous_upper=F(8543935,100000000)
prev_lower=F()
prev_upper=F(1)
for dim in range(1,9):
    J_low=A0;J_up=A0+R_hi**2/13
    for l,(blo,bhi) in enumerate(bounds,1):
        t,s=compression(l,dim)
        assert t<blo  # tail positivity: Hilbert-Schmidt mass exceeds compression trace
        # Positive trace-class C=T*T. P=orthogonal compression onto span tests.
        # tr(C^2) = tr(A^2)+2||B||_HS^2+tr(D^2)
        # <= tr(A^2)+2 tr(A)tr(D)+tr(D)^2 = s+b^2-t^2.
        J_low+=(2*l+1)*s
        J_up+=(2*l+1)*(s+bhi*bhi-t*t)
    low=base+F(6,5)*J_low
    up=base+F(6,5)*J_up
    assert low>prev_lower and up<prev_upper and up<previous_upper
    prev_lower,prev_upper=low,up
    print('DIM',dim,'LOW',format(float(low),'.16g'),'UP',format(float(up),'.16g'))

# Fully rational floor/ceil endpoint assertions; decimals themselves are not proofs.
assert prev_lower>F(85396726,10**9) # 0.085396726
assert prev_upper<F(85438735,10**9) # 0.085438735
assert prev_lower<prev_upper
print('CERTIFIED_INTERVAL := 0.085396726 < p42 < 0.085438735')
print('EXACT_ENDPOINT_HASH :=',hashlib.sha256((str(prev_lower)+'|'+str(prev_upper)).encode()).hexdigest())
print('HARMONICS := ell 1..5; dimension 8; tail ell>=6 via R^2/13')
print('SOURCE_THEOREM_DEPENDENCIES := 4-point reduction, l0 trace, b_l values, harmonic action')
print('FULL_E_J2 := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
print('RESULT := COMPUTATION_PASS')