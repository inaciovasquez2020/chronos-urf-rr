#!/usr/bin/env python3
"""Exact geometric envelope for first birth from random Minkowski sprinklings.

Standard library only. Reproducible bounded checks; proofs are in companion MD.
No Git operations, downloads, or external dependencies.
"""
import math
from fractions import Fraction as F
from itertools import product


def bounds(N, S, future):
    assert N >= 2 and 0 <= S and 0 <= future and S + future <= 1
    p = future / (1-S)
    lower = (1-S)**(N-1) * sum(p**j for j in range(N))
    upper = (1-S)**(N-1) * (1+(N-1)*p)
    return lower, upper


def brute_multinomial(N, S, future):
    # Independent status of N-1 other events: PAST, FUTURE, INCOMPARABLE.
    probs = (S, future, 1-S-future)
    lower = upper = F(0)
    for states in product(range(3), repeat=N-1):
        weight = math.prod(probs[i] for i in states)
        if 0 in states: continue  # x is not minimal
        f = states.count(1)
        lower += weight * F(N, N-f)       # density = N * first-birth probability
        upper += weight * (f+1)           # density = N * first-birth probability
    return lower, upper


def diamond_volume(s):
    u, w = s
    S = (u*w)**2
    future = ((1-u)*(1-w))**2
    return S, future


def future_strip_bound(N, eps):
    assert N>=3 and 0 < eps <= .5
    return 6*math.sqrt(math.pi)/math.sqrt(N-2) * (eps+(N-1)*eps**3/3)


def integrate_2d_grid(N, lo=0, hi=1, steps=800):
    # Deterministic midpoint quadrature for L/U over the 4D diamond.
    # µ density = 12 (u-w)^2 du dw, triangular 0<w<u<1.
    L=U=0.0
    for i in range(steps):
        u=lo+(hi-lo)*(i+.5)/steps
        for j in range(steps):
            w=u*(j+.5)/steps
            S, f=diamond_volume((u,w))
            l, h=bounds(N,S,f)
            volume_weight=12*(u-w)**2*u*(hi-lo)/steps**2
            L+=l*volume_weight; U+=h*volume_weight
    return L,U


def main():
    checks=0
    for N in range(2,7):
        for S, Fu in ((F(0),F(0)), (F(0),F(1)), (F(1,5),F(1,4)),
                      (F(1,3),F(1,6)), (F(1,2),F(0)), (F(1,10),F(3,4))):
            low,high=bounds(N,S,Fu)
            brute_l,brute_u=brute_multinomial(N,S,Fu)
            assert low == brute_l and high == brute_u, (N,S,Fu,low,brute_l,high,brute_u)
            assert low<=high
            checks+=1
    assert checks==30
    print('EXACT_MULTINOMIAL_IDENTITIES := PASS',checks)
    # N=2 is exact: all possible 2-point posets have the same geometric first-birth law.
    for S,Fu in ((F(1,5),F(1,4)),(F(0),F(1)),(F(1,4),F(0))):
        a,b=bounds(2,S,Fu)
        assert a==b==1-S+Fu
    print('TWO_EVENT_SPATIAL_DENSITY := 1-S+F EXACT')
    for N in (2,3,4,8,16):
        L,U=integrate_2d_grid(N,steps=150)
        assert L < 1.001 and U > .999, (N,L,U)
        print('GLOBAL_ENVELOPE N=%d LOWER_INTEGRAL=%.8f UPPER_INTEGRAL=%.8f'%(N,L,U))
    for N in (1000,10000,1000000):
        eps=N**(-.2)
        print('FUTURE_NULL_STRIP N=%d eps=%.6g PROBABILITY_UPPER_BOUND=%.6g'%(
            N,eps,future_strip_bound(N,eps)))
    print('GEOMETRIC_FIRST_BIRTH_ENVELOPE := PROVED_BY_COUNTING')
    print('ASYMPTOTIC_MINKOWSKI_PREFIX_SAMPLING := OPEN')


if __name__=='__main__':
    main()
