#!/usr/bin/env python3
"""Bounded reproducible expected-intensity simulation for shallow-past future marks.
No repository mutation, network or dependencies. Not a sample of extension-selected births.
"""
from random import Random
from fractions import Fraction

seed=20261111
rng=Random(seed)
K=450000
for N,j in ((1000,0),(10000,0),(10000,1)):
    weight=0.; meanfuture=0.; future2=0.; large=0.; shellmass=0.
    for _ in range(K):
        u=rng.random()**.25
        w=u*(1-rng.random()**(1/3))
        s=(u*w)**2
        f=((1-u)*(1-w))**2
        prob=(1-s)**(N-1)
        if j:
            prob=(N-1)*s*(1-s)**(N-2)
        p=f/(1-s)
        eV=(N-1-j)*p/N
        eV2=((N-1-j)*p*(1-p)+(N-1-j)**2*p*p)/N**2
        weight+=prob
        meanfuture+=prob*eV
        future2+=prob*eV2
        large+=prob*(p>=.25)
        shellmass+=prob*(u>=.5)
    meanfuture/=weight;future2/=weight;large/=weight;shellmass/=weight
    print(f'N={N} j={j} sampling_K={K} expected_shallow_count={N*weight/K:.5f} '
          f'normalized_future_mean={meanfuture:.6f} future_2moment={future2:.6f} '
          f'future_fraction_ge_1/4_proxy={large:.6f} null_u_ge_half={shellmass:.6f}',flush=True)
    assert 0 <= meanfuture <= 1
    assert 0 <= future2 <= meanfuture
    assert 0 <= large <= 1
    assert 0 <= shellmass <= 1
assert Fraction(1, (1+1)*(2*1+1)) == Fraction(1,6)
assert Fraction(1, (2+1)*(2*2+1)) == Fraction(1,15)
print('MARKED_EXPECTED_INTENSITY_DIAGNOSTICS := FINITE_MC_PASS')
print('LINEAR_EXTENSION_SELECTION_WEIGHT_LIMIT := OPEN')
