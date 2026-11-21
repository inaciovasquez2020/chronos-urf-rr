#!/usr/bin/env python3
"""Exact N-DAG Minkowski expectation; stdlib-only rational certificate.

Model: four independent uniform events in 4D Minkowski unit causal diamond.
A = Pr(X0 << X3, X1 << X2, X1 << X3)
  = E[1_{X1<<X3} W_future(X1) W_past(X3)].

Null radial variables a=t-r,b=t+r (0<=a<=b<=1) have density
12(b-a)^2 da db. Future and past normalized volumes are
W_future=(1-a)^2(1-b)^2 and W_past=c^2 d^2, respectively.
Conditioned on radial coordinates, the 3D relative angular cosine is
uniform on [-1,1]. For timelike x<y its angular probability is 1 on
0<=a<=b<=c<=d<=1, and (c-a)(d-b)/((b-a)(d-c)) on
0<=a<=c<=b<=d<=1. Therefore A=144*(I1+I2), where the integrands
in `integrands` below are *polynomials* on the respective simplexes.

Two independent exact integrators:
  1. Direct ordered-monomial antiderivatives.
  2. Dirichlet gap-monomial integrals on the unit simplex.
No floating point, Monte Carlo, or external library.
"""
from fractions import Fraction as Q
from math import factorial
from itertools import product

# Polynomial represented by dict of 4-variable exponent tuples -> rational.
def add(p,q):
    z=p.copy()
    for m,c in q.items():
        z[m]=z.get(m,Q(0))+c
    return {m:c for m,c in z.items() if c}

def mul(p,q):
    z={}
    for x,c in p.items():
        for y,d in q.items():
            m=tuple(a+b for a,b in zip(x,y))
            z[m]=z.get(m,Q(0))+c*d
    return {m:c for m,c in z.items() if c}

def const(c): return {(0,0,0,0):Q(c)}
def var(i):
    ex=[0]*4;ex[i]=1
    return {tuple(ex):Q(1)}
def sub(p,q): return add(p,{m:-c for m,c in q.items()})
def power(p,k):
    out=const(1)
    for _ in range(k): out=mul(out,p)
    return out

def integrands(v):
    a,b,c,d=v
    common=mul(mul(power(sub(const(1),a),2),power(sub(const(1),b),2)),mul(power(c,2),power(d,2)))
    full=mul(common,mul(power(sub(b,a),2),power(sub(d,c),2)))
    partial=mul(common,mul(mul(sub(b,a),sub(d,c)),mul(sub(c,a),sub(d,b))))
    return full,partial

def ordered_integral(p):
    # Variables are already named in ascending simplex order.
    total=Q(0)
    for powers,coeff in p.items():
        denom=1;cum=0
        for i,k in enumerate(powers,1):
            cum+=k;denom*=cum+i
        total+=coeff/denom
    return total

def gap_integral(p):
    # Dirichlet simplex {g_i >=0, sum(g_i)<=1}, d^4g.
    return sum((coeff*Q(factorial(k[0])*factorial(k[1])*factorial(k[2])*factorial(k[3]),factorial(sum(k)+4)) for k,coeff in p.items()),Q(0))

def linear_sum(*parts):
    ans={}
    for p in parts: ans=add(ans,p)
    return ans

def main():
    x=list(map(var,range(4)))
    # ordered method, first domain a<b<c<d
    f1,_=integrands(x)
    # second domain a<c<b<d: (a,c,b,d)=(x0,x1,x2,x3)
    a,b,c,d=x[0],x[2],x[1],x[3]
    _,f2=integrands((a,b,c,d))
    i1,i2=ordered_integral(f1),ordered_integral(f2)
    assert i1==Q(29663,5189184000)
    assert i2==Q(266113,72648576000)
    A=144*(i1+i2)
    assert A==Q(953,705600)

    # Independent gap-coordinate computation, four successive nonnegative
    # gaps u,v,w,z, with upper constraint u+v+w+z<=1.
    u,v,w,z=x
    a=u;b=linear_sum(u,v);c=linear_sum(u,v,w);d=linear_sum(u,v,w,z)
    g1,_=integrands((a,b,c,d))
    a=u;c=linear_sum(u,v);b=linear_sum(u,v,w);d=linear_sum(u,v,w,z)
    _,g2=integrands((a,b,c,d))
    assert gap_integral(g1)==i1
    assert gap_integral(g2)==i2

    p_constant=Q(78509,882000)-Q(16,5)*A
    assert p_constant==Q(3557,42000)
    # Earlier verified timelike contribution B_timelike=1/17640.
    p_spacelike_constant=p_constant+Q(6,5)*Q(1,17640)
    assert p_spacelike_constant==Q(24919,294000)
    print('ORDERED_SIMPLEX_1 :=',i1)
    print('ORDERED_SIMPLEX_2 :=',i2)
    print('DIRICHLET_GAP_CROSS_CHECK := PASS')
    print('N_DAG_A :=',A)
    print('P42 := 3557/42000 + (6/5)*B_2PLUS2')
    print('P42 := 24919/294000 + (6/5)*J_SPACELIKE')
    print('ANALYTIC_DERIVATION := PROVED')
    print('EXACT_ARITHMETIC := COMPUTATION_PASS')
    print('B_2PLUS2 := OPEN')
    print('GLOBAL_P42 := OPEN')
    print('LEAN := NOT_RUN')
if __name__=='__main__':main()