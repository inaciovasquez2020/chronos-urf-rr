#!/usr/bin/env python3
"""Exact finite-arithmetic certificate for the 4D Minkowski p_(4,2) value.

CONDITIONAL DEPENDENCIES:
  (1) positive-DAG 219-poset identity
      p42 = 24919/294000 + (6/5) J.
  (2) exact 4D conditional future-volume formula (previously audited).
  (3) null-coordinate/scale/ratio transformation derived in proof note.

From these,
J = 72 int_{r,h,q: 0<r<q<1, 0<h<1}
       [ r^4 h^4/(1-r*h) * (1/7-(r+h)/8+r*h/9)
         * q^5 * (-r+q*(3+r*h)/2-h*q^2)^2 ] dr dh dq.

Integrate q, expand in r,h; each monomial r^m h^n/(1-rh)
has exact integral using harmonic numbers and zeta(2).
No SymPy, SciPy, Lean, floating-point approximation, or user repo writes.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import factorial

# 3-variable sparse polynomials: exponents of (r,h,q)
def term(c, e=(0,0,0)):
    return {e:F(c)} if c else {}
def add(*ps):
    z=defaultdict(F)
    for p in ps:
        for e,c in p.items():z[e]+=c
    return {e:c for e,c in z.items() if c}
def scale(p,c):return {e:v*c for e,v in p.items() if v*c}
def mul(a,b):
    z=defaultdict(F)
    for e,c in a.items():
        for f,d in b.items():z[tuple(e[i]+f[i] for i in range(3))]+=c*d
    return {e:c for e,c in z.items() if c}
def power(p,n):
    v=term(1)
    for _ in range(n):v=mul(v,p)
    return v
r=term(1,(1,0,0));h=term(1,(0,1,0));q=term(1,(0,0,1))
S=add(scale(r,-1),scale(q,F(3,2)),scale(mul(r,mul(h,q)),F(1,2)),scale(mul(h,power(q,2)),-1))
poly=mul(power(r,4),mul(power(h,4),mul(add(term(F(1,7)),scale(r,F(-1,8)),scale(h,F(-1,8)),scale(mul(r,h),F(1,9))),mul(power(q,5),power(S,2)))))
poly=scale(poly,72)
# Integrate q from r to 1: r^i*h^j*q^k -> r^i*h^j*(1-r^(k+1))/(k+1)
coef=defaultdict(F)
for (i,j,k),c in poly.items():
    coef[(i,j)]+=c/F(k+1)
    coef[(i+k+1,j)]-=c/F(k+1)
coef={e:c for e,c in coef.items() if c}

def harmonic(n,p=1):return sum((F(1,k**p) for k in range(1,n+1)),F(0))
rat=F(0); zeta2=F(0)
for (m,n),c in coef.items():
    if m==n:
        zeta2+=c
        rat-=c*harmonic(m,2)
    else:
        rat+=c*(harmonic(n)-harmonic(m))/F(n-m)
assert rat==F(-3316139,88200),rat
assert zeta2==F(160,7),zeta2
# zeta2=pi²/6; J = (-3316139+336000*pi²)/88200.
assert zeta2/F(6)==F(80,21)
# p42 = 24919/294000+(6/5)*J.
p_rat=F(24919,294000)+F(6,5)*rat
p_pi2=F(6,5)*zeta2/F(6)
assert p_rat==F(-13239637,294000)
assert p_pi2==F(32,7)
print('STDLIB_EXACT_POLYNOMIAL_Q_INTEGRAL := PASS')
print('NONZERO_2D_MONOMIALS :=',len(coef))
print('HARMONIC_SUM_EVALUATION := PASS')
print('J := (-3316139 + 336000*pi^2)/88200')
print('P42 := (-13239637 + 1344000*pi^2)/294000')
print('NUMERICAL_VALIDATION := SEE_INDEPENDENT_GAUSS_CERTIFICATE')
print('NOVELTY := NOT_ESTABLISHED')
print('LEAN := NOT_RUN')
print('REPOSITORY := UNCHANGED')