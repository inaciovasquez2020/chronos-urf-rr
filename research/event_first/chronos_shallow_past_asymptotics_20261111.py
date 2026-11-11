#!/usr/bin/env python3
"""4D Minkowski-diamond causal-past volume distribution and shallow-past asymptotic.
No external dependencies. Numerical validation does not establish the asymptotic theorem.
"""
import math
import random
from statistics import mean


def cdf(s):
    if s <= 0: return 0.0
    if s >= 1: return 1.0
    return 6*math.sqrt(s)-3*s+3*s*math.log(s)-2*s**1.5


def exact_expected_shallow(N, n):
    assert 1 <= n <= N
    harmonic_N = sum(1.0/j for j in range(1, N+1))
    harmonic_j = 0.0
    total = 0.0
    for j in range(n):
        if j: harmonic_j += 1.0/j
        log_comb = math.lgamma(N)-math.lgamma(j+1)-math.lgamma(N-j)
        log_beta = math.lgamma(j+0.5)+math.lgamma(N-j)-math.lgamma(N+0.5)
        positive = math.exp(log_comb+log_beta) * (N-j)/(N+0.5)
        total += 3*N*positive + 3*(harmonic_j-harmonic_N)
    return total


def asymptotic_coefficient(n):
    return 3*sum(math.gamma(j+0.5)/math.factorial(j) for j in range(n))


def sampled_past_fraction(rng):
    # Diamond from t=-1 to t=1. Spatial dimension three.
    a = 1-rng.random()**.25
    t = a if rng.random() < 0.5 else -a
    r = (1-a)*rng.random()**(1/3)
    # Past diamond proper duration normalized by endpoint separation 2.
    return (((1+t)**2-r*r)/4)**2


def main():
    for s in (.0001,.001,.01,.1,.25,.5,.9):
        assert 0 < cdf(s) < 1
        assert cdf(s) <= 6*math.sqrt(s)+1e-12
    assert abs(exact_expected_shallow(1,1)-1)<1e-12
    assert abs(exact_expected_shallow(2,1)-1.9)<1e-12
    for N in (2,3,8,16,100):
        assert abs(exact_expected_shallow(N,N)-N)<1e-9
    rng=random.Random(20261111)
    sample=[sampled_past_fraction(rng) for _ in range(160000)]
    for s in (.001,.01,.1,.5):
        emp=sum(x<=s for x in sample)/len(sample)
        theoretical=cdf(s)
        assert abs(emp-theoretical)<.007,(s,emp,theoretical)
        print('CDF s=',s,'emp=',round(emp,6),'exact=',round(theoretical,6))
    for n in (1,2,3,5):
        c=asymptotic_coefficient(n)
        for N in (100,1000,10000):
            value=exact_expected_shallow(N,n)
            print('SHALLOW_EXPECTATION N=',N,'n=',n,'value=',round(value,6),
                  'normalized=',round(value/math.sqrt(N),6),'limit=',round(c,6))
    print('CDF_ANALYTIC_FORMULA := NUMERIC_CHECK_PASS')
    print('BETA_HARMONIC_FINITE_FORMULA := CHECK_PASS')
    print('SHALLOW_PAST_SQRT_SCALING := PROVED_ANALYTICALLY_NOT_LEAN')
    print('LINEAR_EXTENSION_PREFIX_SELECTION := OPEN')


if __name__ == '__main__':
    main()
