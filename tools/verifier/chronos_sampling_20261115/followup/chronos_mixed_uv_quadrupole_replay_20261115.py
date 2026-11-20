#!/usr/bin/env python3
"""Exact ell=2 mixed U,V causal-cap matrix. Source reproduced from 2026-11-15 archived certificate."""
from sympy import symbols, Poly, Rational, expand, Matrix, simplify
from functools import lru_cache
c,d,u,v=symbols('c d u v')
def square_integral(p):
    return sum((coef/Rational((e[0]+1)*(e[1]+1)) for e,coef in Poly(p,u,v).terms()),Rational(0))
def triangle(p):
    return sum((coef/Rational((e[0]+1)*(sum(e)+2)) for e,coef in Poly(p,c,d).terms()),Rational(0))
@lru_cache(None)
def action(i,j):
    a=c*u
    b=c+(d-c)*v
    q=(1-u)*v*(1-v)*(d-a)*(b-a)*(a*b)**(2*i)*((1-a)*(1-b))**(2*j)*((b-a)-2*c*(1-u)*(1-v))
    return expand(3*c*c*(d-c)*square_integral(q))
@lru_cache(None)
def gram(i,j,k,l):
    return triangle(Rational(3,4)*(d-c)**6*(c*d)**(2*(i+k))*((1-c)*(1-d))**(2*(j+l)))
@lru_cache(None)
def energy(i,j,k,l):
    return triangle(12*(d-c)**2*action(i,j)*action(k,l))
def kappa(k):
    ell=2
    return Rational(12,(ell+1)*(4*k+ell+4))*(Rational(1,2*k+1)-Rational(1,2*k+2)-Rational(1,2*k+ell+2)+Rational(1,2*k+ell+3))
if __name__=="__main__":
    ms=((0,0),(1,0),(0,1),(2,0),(1,1),(0,2))
    for i,j in ms:
        if j==0:
            assert simplify(action(i,j)-kappa(i)*(d-c)**2/Rational(4)*(c*d)**(2*i+2))==0
    G=Matrix([[gram(*a,*b) for b in ms] for a in ms])
    B=Matrix([[energy(*a,*b) for b in ms] for a in ms])
    assert G==G.T and B==B.T and G.det()!=0
    X=G.inv()*B
    assert X.trace()>0 and (X*X).trace()>0
    print("QUADRUPOLE_DEGREE2 := PASS")
