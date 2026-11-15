#!/usr/bin/env python3
"""Exact mixed U,V dipole (ell=1) angular compression; no numerical quadrature.

Uses SymPy exact polynomial arithmetic. Does not prove full p42 or asymptotics.
Normalizations: radial probability dmu=12(b-a)^2 da db, r=(b-a)/2,
U=(ab)^2, V=((1-a)(1-b))^2, angular lambda_1=f(1-f).
"""
from sympy import symbols, Poly, Rational, expand, factor, simplify, Matrix
from math import factorial
from functools import lru_cache
import sys

c,d,u,v = symbols('c d u v')

def unit_square(poly):
    return sum((coef/Rational((e[0]+1)*(e[1]+1)) for e,coef in Poly(expand(poly),u,v).terms()),Rational(0))

def triangle(poly):
    # Integral over 0<c<d<1. Substitute c=d*w, integrate w,d from 0 to1.
    w=symbols('w')
    p=Poly(expand(poly),c,d)
    return sum((coef/Rational((exp[0]+1)*(sum(exp)+2)) for exp,coef in p.terms()),Rational(0))

@lru_cache(None)
def action(i,j):
    # causal partial-angular cap: a<c<b<d; angular eigenvalue lambda1=f(1-f),
    # f=(c-a)(d-b)/[(b-a)(d-c)], 1-f=(b-c)(d-a)/[(b-a)(d-c)].
    # a=c*u, b=c+(d-c)*v, then (b-a)^2 cancels denominator exactly.
    a=c*u
    b=c+(d-c)*v
    P=(1-u)*v*(1-v)*(d-a)*(b-a)*(a*b)**(2*i)*((1-a)*(1-b))**(2*j)
    val=factor(6*c*c*(d-c)*unit_square(P))
    assert simplify(val.subs(d,c))==0
    return val

@lru_cache(None)
def gram(i,j,k,l):
    U=(c*d)**2; V=((1-c)*(1-d))**2
    return triangle(Rational(3)*(d-c)**4*U**(i+k)*V**(j+l))

@lru_cache(None)
def energy(i,j,k,l):
    return triangle(expand(12*(d-c)**2*action(i,j)*action(k,l)))

def kappa(k):
    return Rational(6,4*k+5)*(Rational(1,2*k+1)-Rational(1,2*k+2)-Rational(1,2*k+3)+Rational(1,2*k+4))

def report(mons):
    for i,j in mons:
        a=action(i,j)
        print('ACTION',i,j, 'degree',Poly(expand(a),c,d).total_degree(), 'terms',len(Poly(expand(a),c,d).terms()),flush=True)
        if j==0:
            predicted=kappa(i)*((d-c)/2)*(c*d)**(2*i+2)
            assert simplify(a-predicted)==0, (i,j,a,predicted)
            print('  ONE_VARIABLE_IDENTITY := PASS',flush=True)
    G=Matrix([[gram(*x,*y) for y in mons] for x in mons])
    B=Matrix([[energy(*x,*y) for y in mons] for x in mons])
    assert G==G.T and B==B.T
    assert G.det()!=0
    X=G.inv()*B
    t=X.trace()
    s=(X*X).trace()
    assert t>0 and s>0 and s<=t*t
    print('MONOMIALS :=',mons)
    print('GRAM_G :=',G.tolist())
    print('ENERGY_B :=',B.tolist())
    print('T_EXACT :=',t)
    print('S_EXACT :=',s)
    print('T_DECIMAL :=',t.evalf(17))
    print('S_DECIMAL :=',s.evalf(17))
    return t,s

if __name__=='__main__':
    # include (0,0),(1,0),(0,1): full bivariate degree 1
    t,s=report(((0,0),(1,0),(0,1)))
    # independent analytic b1 mass formula: 6 pi² - 829/14.
    # numerical outputs below are diagnostic only; exact bound requires rational pi interval.
    import sympy as sp
    b1=6*sp.pi**2-sp.Rational(829,14)
    assert bool(t<b1)
    print('B1_MINUS_T_APPROX :=',(b1-t).evalf(16))
    print('CONDITIONAL_A1_LOWER :=', (3*s).evalf(16))
    print('L1_MIXED_UV_EXACT := PASS')
    print('FULL_FOUR_POINT_PROBABILITY := OPEN')