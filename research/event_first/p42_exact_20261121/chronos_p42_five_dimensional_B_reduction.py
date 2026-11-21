#!/usr/bin/env python3
"""Five-variable global representation of the 2+2 DAG expectation B.

Normalized unit Minkowski diamond D=I((0,0),(1,0)), volume pi/24.
Let m(t)=min(t,1-t), x=(t,r*n), y=(s,w*mhat), mu=n.mhat.
All radial-time position densities integrate with 96*r² dr dt and
relative direction mu has density dmu/2. Define for u=R-x, v=R-y:
 a²=(1-t)²-r², c²=(1-s)²-w²,
 g=(1-t)(1-s)-r*w*mu, b=g/a, d=sqrt(b²-c²).
The common future volume is V=pi*f(a,b,d), where f is the exact
coaxial polygon expression. Then
 B=(96²/2)*Integral_{t,s in [0,1], r in [0,m(t)],
    w in [0,m(s)], mu in [-1,1]} r²*w²*(24*f(a,b,d))²
    dmu dw dr ds dt.

A value of B cannot be inferred without evaluating this final integral.
"""
from fractions import Fraction as Q
from math import pi, sqrt
from pathlib import Path
import importlib.util

p=Path(__file__).with_name('chronos_p42_lorentz_three_cone_certificate.py')
spec=importlib.util.spec_from_file_location('lorentz',p)
L=importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)


def geometry(t,r,s,w,mu):
    t,r,s,w,mu=map(float,(t,r,s,w,mu))
    assert 0<t<1 and 0<s<1 and 0<=r<min(t,1-t) and 0<=w<min(s,1-s)
    assert -1<=mu<=1
    a2=(1-t)**2-r*r
    c2=(1-s)**2-w*w
    g=(1-t)*(1-s)-r*w*mu
    a=sqrt(a2); b=g/a
    d2=max(0,b*b-c2)
    return a,b,sqrt(d2)


def independent_geometry(t,r,s,w,mu):
    # Direct Minkowski products of x,y,R in a common cartesian frame.
    from math import sqrt as sq
    x=(t,r,0.,0.)
    y=(s,w*mu,w*sq(1-mu*mu),0.)
    R=(1.,0.,0.,0.)
    u=L.sub(R,x);v=L.sub(R,y)
    uu=L.dot(u,u);uv=L.dot(u,v);vv=L.dot(v,v)
    return sq(uu),uv/sq(uu),sq(max(0,(uv/sq(uu))**2-vv))


def check():
    # Exact integral of radial-time density, independently of angular density.
    # integral_0^1 integral_0^{min(t,1-t)} 96*r² dr dt = 1.
    assert Q(96,3)*2*Q(1,2)**4/Q(4)==1
    # independent angular normalization: integral_{-1}^1 dmu/2 =1.
    assert Q(1,2)*2==1
    from random import Random
    rng=Random(20261121)
    count=0
    maxgeom=0.
    for _ in range(100):
        t=.1+.8*rng.random();s=.1+.8*rng.random()
        r=rng.random()*min(t,1-t)*.98
        w=rng.random()*min(s,1-s)*.98
        mu=2*rng.random()-1
        val=geometry(t,r,s,w,mu)
        other=independent_geometry(t,r,s,w,mu)
        maxgeom=max(maxgeom,max(abs(a-b) for a,b in zip(val,other)))
        assert max(abs(a-b) for a,b in zip(val,other))<1e-10
        count+=1
    print('DIAMOND_VOLUME := pi/24')
    print('RADIAL_TIME_DENSITY_NORMALIZATION := PASS (exact rational)')
    print('PAIR_ANGULAR_DENSITY_NORMALIZATION := PASS (exact rational)')
    print('FIVE_VARIABLE_INVARIANTS := PASS',count)
    print('MAX_INVARIANT_FLOAT_DISCREPANCY :=',maxgeom)
    print('GLOBAL_REPRESENTATION := ANALYTICALLY_DERIVED')
    print('GLOBAL_INTEGRAL_EVALUATION := NOT_RUN')
    print('EXACT_B_AND_P42 := OPEN')

if __name__=='__main__': check()