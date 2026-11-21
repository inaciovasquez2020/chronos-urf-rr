#!/usr/bin/env python3
"""Lorentz-covariant reduction of a 3+1 dimensional triple-cone four-volume.

For future-timelike u=R-x and v=R-y, set
 a=sqrt(u.u), b=(u.v)/a, d=sqrt(b*b-v.v).
In the rest frame of u, rotate the spatial part of v onto the x-axis:
 x=(-a,0), y=(-b,d), R=0.
The original volume equals the coaxial rational polygon volume with
(t0,c0,t1,c1,T,C)=(-a,0,-b,d,0,0).
Exact algebraic invariance checks and independent quasi-Monte Carlo tests.
Not an exact calculation of the remaining expectation B or p_(4,2).
"""
from fractions import Fraction as Q
from math import pi, sqrt, sin, cos
from pathlib import Path
import importlib.util

p=Path(__file__).with_name('chronos_p42_coaxial_three_cone_spacetime.py')
spec=importlib.util.spec_from_file_location('coaxial',p)
coax=importlib.util.module_from_spec(spec)
spec.loader.exec_module(coax)

def dot(a,b):return a[0]*b[0]-sum(x*y for x,y in zip(a[1:],b[1:]))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def boost_y(q):
    # exact rational Lorentz boost along y, velocity 3/5, gamma 5/4
    t,x,y,z=q
    return (Q(5,4)*t+Q(3,4)*y, x, Q(3,4)*t+Q(5,4)*y,z)
def rotate_x_y(q):
    t,x,y,z=q
    return (t,Q(3,5)*x-Q(4,5)*y,Q(4,5)*x+Q(3,5)*y,z)

def inv(x,y,R):
    u=sub(R,x);v=sub(R,y)
    return dot(u,u),dot(u,v),dot(v,v)

def canonical_volume(a,b,d):
    return coax.cone_volume_over_pi(-a,0,-b,d,0,0)

def exact_invariance():
    configs=[(Q(1),Q(1),Q(1,2)),(Q(6,5),Q(4,5),Q(2,5)),
             (Q(3,2),Q(5,4),Q(1,2)),(Q(5,4),Q(7,5),Q(3,4))]
    for a,b,d in configs:
        assert a>0 and b>d>=0
        x=(-a,Q(0),Q(0),Q(0))
        y=(-b,d,Q(0),Q(0))
        R=(Q(0),)*4
        baseline=inv(x,y,R)
        transformed=[rotate_x_y(boost_y(z)) for z in (x,y,R)]
        assert inv(*transformed)==baseline
        assert dot(sub(x,y),sub(x,y))==dot(sub(transformed[0],transformed[1]),sub(transformed[0],transformed[1]))
        assert canonical_volume(a,b,d)>=0
    print('EXACT_RATIONAL_LORENTZ_INVARIANCE := PASS (4 configurations)')
    return configs

def qmc_test(a=Q(1),b=Q(1),d=Q(1,2),power=18):
    # Independent 4D integral: uniform points in I(x,R), count those in J+(y).
    # The time coordinate t in [0,1] has normalized density 32*min(t,1-t)^3.
    from scipy.stats import qmc
    import numpy as np
    generator=qmc.Sobol(d=4,scramble=True,seed=20261121)
    w=generator.random_base2(power)
    u=w[:,0]
    tau=np.where(u<=0.5,(u/8.)**0.25,1.-((1.-u)/8.)**0.25)
    radial=np.minimum(tau,1.-tau)*w[:,1]**(1./3.)
    costh=2*w[:,2]-1
    az=2*np.pi*w[:,3]
    st=np.sqrt(1-costh*costh)
    px=radial*st*np.cos(az);py=radial*st*np.sin(az);pz=radial*costh
    t=-float(a)+float(a)*tau # scale for interval from -a to 0
    px*=float(a);py*=float(a);pz*=float(a)
    future=(t>=-float(b)) & ((t+float(b))**2 >= (px-float(d))**2+py**2+pz**2)
    ratio=future.mean()
    empirical=ratio*(np.pi*float(a)**4/24)
    exact=float(canonical_volume(a,b,d))*np.pi
    print('FOUR_DIMENSIONAL_QMC_N :=',len(w))
    print('QMC_VOLUME :=',empirical)
    print('EXACT_POLYGON_VOLUME :=',exact)
    print('QMC_ABS_ERROR :=',abs(empirical-exact))
    assert abs(empirical-exact) < 2e-4
    print('INDEPENDENT_SAMPLER_CONSISTENCY := PASS (not rigorous error bound)')

def main():
    exact_invariance()
    a,b,d=Q(1),Q(1),Q(1,2)
    print('SPACELIKE_PAIR_EXACT_VOLUME_OVER_PI :=',canonical_volume(a,b,d))
    assert d*d>(a-b)**2
    qmc_test(a,b,d)
    print('THREE_CONE_VOLUME_REDUCTION := ANALYTICALLY_PROVED')
    print('FULL_EXPECTATION_B := OPEN')
    print('P42 := OPEN')

if __name__=='__main__':main()
