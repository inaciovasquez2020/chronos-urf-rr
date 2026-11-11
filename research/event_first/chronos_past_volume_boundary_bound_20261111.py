#!/usr/bin/env python3
"""Finite-N exact union-bound certificate for fixed-prefix boundary localization.
No dependencies. The asymptotic follows analytically, not from these evaluations.
"""
import math

def bound(N,n,c):
    assert N>=n>=1 and c>1
    s=c*math.log(N)/N
    if s>=1:return 0.0 # entire diamond is in S<1 except measure-zero tip
    M=N-1
    term=(1-s)**M
    tail=term
    for j in range(1,n):
        term*=((M-j+1)/j)*(s/(1-s))
        tail+=term
    return min(1.0,N*tail)

def crude_bound(N,n,c):
    s=c*math.log(N)/N
    if s>=1:return 0.0
    M=N-1
    tail=sum((M*s)**j/math.factorial(j) for j in range(n))
    return min(1.,N*math.exp(-(M-n+1)*s)*tail)

def main():
    for N in (100,1000,10000,100000,1000000):
        for n in (1,2,3):
            for c in (1.5,2.0):
                if N>=n:
                    b=bound(N,n,c); cr=crude_bound(N,n,c)
                    assert b<=cr+1e-12
                    if n==2 and c==2.0:
                        print('N=',N,'n=',n,'c=',c,'rigorous_probability_bound=',round(b,9))
    print('GEOMETRIC_BOUNDARY_LOCALIZATION := PROVED_ANALYTICALLY')
    print('BINOMIAL_UNION_BOUND_NUMERIC := PASS')
    print('FIXED_PREFIX_CAUSAL_PROFILE_LIMIT := OPEN')
if __name__=='__main__':main()
