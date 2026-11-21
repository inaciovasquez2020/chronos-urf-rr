#!/usr/bin/env python3
"""Derive exact global Chronos spacelike 2+2 probability J.
Starts from audited 4D kernel, uses null-coordinate scale/ratio transforms.
All symbolic coefficients exact rational. Compare independent Gaussian quadrature.
"""
import sympy as s
from fractions import Fraction
from math import pi
r,h,q=s.symbols('r h q',positive=True)
T=-r+q*(3+r*h)/2-h*q*q
K=s.integrate(q**5*T**2,(q,r,1))
M=s.expand(72*r**4*h**4*(s.Rational(1,7)-(r+h)/8+r*h/9)*K)
P=s.Poly(M,r,h)
assert P.total_degree()<=28

H=lambda n:sum((s.Rational(1,k) for k in range(1,n+1)),s.Rational(0))
H2=lambda n:sum((s.Rational(1,k*k) for k in range(1,n+1)),s.Rational(0))
R=s.Rational(0); Z=s.Rational(0)
for (m,n),coef in P.terms():
    # E_mn = int_0^1 int_0^1 r^m h^n/(1-rh) dr dh
    if m==n:
        R-=coef*H2(m)
        Z+=coef
    else:
        R+=coef*(H(n)-H(m))/s.Integer(n-m)
J=s.factor(R+Z*s.zeta(2))
p42=s.factor(s.Rational(24919,294000)+s.Rational(6,5)*J)
print('MONOMIAL_COUNT :=',len(P.terms()))
print('J_RATIONAL_PART :=',R)
print('J_ZETA2_COEFFICIENT :=',Z)
print('J_EXACT :=',J)
print('P42_EXACT :=',p42)
print('J_NUMERIC_50D :=',s.N(J,50))
print('P42_NUMERIC_50D :=',s.N(p42,50))
assert 0.00050<float(J)<0.00060
assert 0.0853<float(p42)<0.0855
# Independent brute-force deterministic Gauss-Legendre cubature of the
# 3D rational integrand, avoiding the harmonic-sum evaluation path.
import numpy as np
from numpy.polynomial.legendre import leggauss
for n in (18,36,72):
    z,w=leggauss(n); z=(z+1)/2;w=w/2
    rr=z[:,None,None];hh=z[None,:,None];qq=rr+(1-rr)*z[None,None,:]
    integrand=72*rr**4*hh**4/(1-rr*hh)*(1/7-(rr+hh)/8+rr*hh/9)*qq**5*(-rr+qq*(3+rr*hh)/2-hh*qq**2)**2*(1-rr)
    ans=np.sum(integrand*w[:,None,None]*w[None,:,None]*w[None,None,:])
    print('INDEPENDENT_GAUSS_3D_n :=',n,'J :=',repr(float(ans)),'ERROR :=',repr(abs(float(ans)-float(J))))
    if n==72: assert abs(float(ans)-float(J))<3e-10
print('EXACT_GLOBAL_J := ALGEBRAICALLY_DERIVED')
print('EXACT_GLOBAL_P42 := CONDITIONAL_ON_PRIOR_A_AND_DAG_IDENTITY')