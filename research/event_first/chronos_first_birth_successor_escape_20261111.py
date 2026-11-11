#!/usr/bin/env python3
"""Reproducible analytic certificates and Gaussian-scaled quadrature for a 4D causal diamond.

All statements about limits are proved in the companion report, not by quadrature.
Numerical quadrature requires numpy and scipy; no network or repo mutation.
"""
from fractions import Fraction
from math import comb, gamma, pi, sqrt, exp
import numpy as np
from scipy.special import roots_legendre

# Independent exact low-N integration: E[S]=1/20, E[S^2]=1/105, E[SF]=1/2100.
ES = Fraction(1,20); ES2=Fraction(1,105); ESF=Fraction(1,2100)
assert 2*(1-2*ES) == Fraction(9,5)
assert 3*(1-4*ES+2*ES2+2*ESF) == Fraction(123,50)
print('EXACT_E_ISOLATED_N2 := 9/5')
print('EXACT_E_ISOLATED_N3 := 123/50')

# Exact asymptotic marked isolated candidates having exactly ell successors.
# Constant from 12 ∫ exp(-y²) dy ∫ exp(-v²) v^(2ell)/ell! dv.
for ell in range(7):
    c = 3*pi*comb(2*ell,ell)/4**ell
    integral = 3*sqrt(pi)*gamma(ell+.5)/__import__('math').factorial(ell)
    assert abs(c-integral) < 1.e-12
print('CORNER_INTENSITY_CONSTANTS := PASS, ell=0..6')

nodes=200
z,weights=roots_legendre(nodes)
# Gaussian-scaled half-strip 0..8; truncation is below quadrature precision for large N.
grid=4*(z+1); wgt=4*weights
V,Y=np.meshgrid(grid,grid,indexing='ij')
WW=np.outer(wgt,wgt)
for N in [100,1000,10000]:
    U=1-V/sqrt(N)
    W=Y/sqrt(N)
    valid=(U>=0)&(W>=0)&(W<=U)
    s=np.where(valid,(U*W)**2,0)
    f=np.where(valid,((1-U)*(1-W))**2,0)
    a=np.where(valid,1-s-f,0)
    density=12*np.where(valid,(U-W)**2,0)
    vals=[]
    for ell in range(3):
        mass=comb(N-1,ell)*f**ell*np.maximum(a,0)**(N-1-ell)
        actual=float(np.sum(WW*density*mass))
        vals.append(actual)
    print(f'N={N} EXPECTED_ISOLATED_WITH_ELL_SUCCESSORS=',*[round(x,7) for x in vals], 'TARGET=',*[round(3*pi*comb(2*ell,ell)/4**ell,7) for ell in range(3)])

# Constants in the global bound for K <= (N-1)/64.
C=12*sqrt(pi)*(sqrt(8)+sqrt(8*pi))
assert C <167.0
print('UNIFORM_EXPECTED_MARKED_COUNT_BOUND_CONSTANT :=',round(C,7))
print('PROVED_BY_ANALYSIS: Pr(first has <=K successors) <= C*(K+1)^(3/2)/(N-1) + (K+1)*(exp(-9*(N-1)/512)+exp(-(N-1)/16))')
print('VALID_FOR: 0<=K<=(N-1)/64')
print('ASYMPTOTIC: K=o(N^(2/3)) => probability tends 0')
print('MINKOWSKI_PREFIX_PROFILE_LIMIT := OPEN')
