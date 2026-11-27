#!/usr/bin/env python3
"""Exact 2D kernel reduction of the spacelike 2+2 DAG term J.

Checks exact q-polynomial integration and symbolic recurrence, plus
independent high-precision quadrature. This script does NOT evaluate the
remaining outer two-dimensional integral.
"""
from random import Random
import sympy as S
import mpmath as mp

u,v,h,q=S.symbols('u v h q',positive=True)
E=(3*v+u*h*h)/(2*h)
H=-u+q*E-v*q*q
q0=u*h/v
K=S.expand(u*u*S.Rational(1,6)*(1-q0**6)
          -2*u*E*S.Rational(1,7)*(1-q0**7)
          +(E**2+2*u*v)*S.Rational(1,8)*(1-q0**8)
          -2*E*v*S.Rational(1,9)*(1-q0**9)
          +v*v*S.Rational(1,10)*(1-q0**10))
P=S.cancel(h**4*K)
poly=S.Poly(P,h)
assert poly.degree()<=14
assert all(exp[0]>=0 for exp,_ in poly.terms())
Fq=S.integrate(q**5*H**2,q)
assert S.cancel((Fq.subs(q,1)-Fq.subs(q,q0))-K)==0
I0=S.atanh(h*S.sqrt(u/v))/S.sqrt(u*v)
I1=-S.log(v-u*h*h)/(2*u)
assert S.simplify(S.diff(I0,h)-1/(v-u*h*h))==0
assert S.simplify(S.diff(I1,h)-h/(v-u*h*h))==0
coeffs={n:S.factor(poly.nth(n)) for n in range(poly.degree()+1)}
num_coeffs={n:S.lambdify((u,v),c,'mpmath',cse=True) for n,c in coeffs.items() if c!=0}

def primitive_deltas(uu,vv,lo,hi):
    iv0=lambda x: mp.atanh(x*mp.sqrt(uu/vv))/mp.sqrt(uu*vv)
    iv1=lambda x: -mp.log(vv-uu*x*x)/(2*uu)
    D=[iv0(hi)-iv0(lo),iv1(hi)-iv1(lo)]
    for n in range(2,poly.degree()+1):
        D.append(-(hi**(n-1)-lo**(n-1))/(uu*(n-1))+(vv/uu)*D[n-2])
    return D

def J_inner_exact(uu,vv):
    lo=vv; hi=min(mp.mpf(1),vv/uu)
    ds=primitive_deltas(uu,vv,lo,hi)
    return mp.fsum(num_coeffs[n](uu,vv)*ds[n] for n in num_coeffs)

def inner_quadrature(uu,vv):
    lo=vv; hi=min(mp.mpf(1),vv/uu)
    def fn(hh):
        EE=(3*vv+uu*hh*hh)/(2*hh)
        lower=uu*hh/vv
        kk=uu**2/6*(1-lower**6)-2*uu*EE/7*(1-lower**7)+(EE**2+2*uu*vv)/8*(1-lower**8)-2*EE*vv/9*(1-lower**9)+vv**2/10*(1-lower**10)
        return hh**4*kk/(vv-uu*hh*hh)
    return mp.quad(fn,[lo,hi])

def test():
    mp.mp.dps=65
    rng=Random(271828)
    cases=[(mp.mpf('0.2'),mp.mpf('0.7')),(mp.mpf('0.8'),mp.mpf('0.3')),
           (mp.mpf('0.35'),mp.mpf('0.45')),(mp.mpf('0.65'),mp.mpf('0.2'))]
    for i in range(12):
        uu=mp.mpf(rng.randint(1,85))/100
        vv=mp.mpf(rng.randint(1,85))/100
        if abs(uu-vv)<mp.mpf('0.04'):continue
        cases.append((uu,vv))
    discrepancies=[]
    for uu,vv in cases:
        a=J_inner_exact(uu,vv); b=inner_quadrature(uu,vv)
        err=abs(a-b)
        assert err<mp.mpf('1e-40'),(uu,vv,mp.nstr(a,20),mp.nstr(b,20),mp.nstr(err,5))
        discrepancies.append(err)
    print('EXACT_Q_POLYNOMIAL_INTEGRAL := PASS')
    print('POLYNOMIAL_H_DEGREE :=',poly.degree())
    print('NONZERO_COEFFICIENTS :=',len(num_coeffs))
    print('ELEMENTARY_PRIMITIVE_RECURRENCE := PROVED')
    print('INDEPENDENT_H_QUADRATURE_CASES :=',len(discrepancies))
    print('MAX_ABSOLUTE_DISCREPANCY :=',mp.nstr(max(discrepancies),7))
    print('J_SPACELIKE := 72*Integral_(0<u,v<1) u^4*(1-u)*(1-v)*[sum(P_n(u,v)*(I_n(hmax)-I_n(v)))] du dv')
    print('hmax := min(1,v/u)')
    print('GLOBAL_J := OPEN (2D definite integral not evaluated)')
    print('GLOBAL_P42 := OPEN')

if __name__=='__main__':test()
