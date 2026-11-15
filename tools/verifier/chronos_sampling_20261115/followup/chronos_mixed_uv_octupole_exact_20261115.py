#!/usr/bin/env python3
"""Exact rational mixed U,V radial compression for Minkowski causal harmonic ell=3.
No numerical quadrature; no claim that full angular trace is solved.
"""
from functools import lru_cache
from sympy import symbols, Poly, Rational, expand, Matrix, simplify
c,d,u,v=symbols('c d u v')
ELL=3
COEFS=(1,-5,5)

def integrate_square(expr):
    return sum((coef/Rational((e[0]+1)*(e[1]+1)) for e,coef in Poly(expr,u,v).terms()),Rational(0))

def integrate_triangle(expr):
    return sum((coef/Rational((e[0]+1)*(sum(e)+2)) for e,coef in Poly(expr,c,d).terms()),Rational(0))

@lru_cache(None)
def action(i,j):
    a=c*u
    b=c+(d-c)*v
    diff=b-a
    g=sum((Rational(coef)*c**(h+1)*(1-u)**(h+1)*(1-v)**(h+1)*diff**(ELL-h) for h,coef in enumerate(COEFS)),Rational(0))
    inner=v*(d-a)*g*(a*b)**(2*i)*((1-a)*(1-b))**(2*j)
    return expand(Rational(12,2**ELL)*c*(d-c)*integrate_square(inner))

@lru_cache(None)
def gram(i,j,k,l):
    return integrate_triangle(Rational(12,2**(2*ELL))*(d-c)**(2*ELL+2)*(c*d)**(2*(i+k))*((1-c)*(1-d))**(2*(j+l)))

@lru_cache(None)
def energy(i,j,k,l):
    return integrate_triangle(12*(d-c)**2*action(i,j)*action(k,l))

def kappa(k):
    l=ELL
    return Rational(12,(l+1)*(4*k+l+4))*(Rational(1,2*k+1)-Rational(1,2*k+2)-Rational(1,2*k+l+2)+Rational(1,2*k+l+3))

def compress(mons):
    for i,j in mons:
        a=action(i,j)
        print('ACTION',i,j,'degree',Poly(a,c,d).total_degree(),flush=True)
        if j==0:
            expected=kappa(i)*((d-c)/2)**ELL*(c*d)**(2*i+2)
            assert simplify(a-expected)==0, ('one-variable',i,j)
            print('U_ONLY_ACTION_CROSSCHECK PASS',i,flush=True)
    G=Matrix([[gram(*x,*y) for y in mons] for x in mons]);B=Matrix([[energy(*x,*y) for y in mons] for x in mons]);
    assert G==G.T and B==B.T and G.det()!=0
    C=G.inv()*B;t=C.trace();s=(C*C).trace()
    assert 0<s<=t*t
    print('BASIS',mons, 'T',t,'S',s,'T_DEC',t.evalf(18),'S_DEC',s.evalf(18),flush=True)
    return t,s

if __name__=='__main__':
    compress(((0,0),(1,0),(0,1)))
    compress(((0,0),(1,0),(0,1),(2,0),(1,1),(0,2)))
    print('ELL3_MIXED_UV_EXACT := PASS')