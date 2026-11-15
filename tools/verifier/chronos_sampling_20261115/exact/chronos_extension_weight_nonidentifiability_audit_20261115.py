#!/usr/bin/env python3
"""Read-only, stdlib-only regression for full fixed-j predecessor profile nonidentifiability.
All claimed first-two probabilities are exact Fraction values. The c_j floors
are computed with floating-point approximations solely to choose finite fixtures.
This is not a proof of or counterexample within 4D Minkowski sprinklings.
"""
from fractions import Fraction
from itertools import permutations
from math import factorial
from chronos_matching_all_fixed_predecessor_counts_counterexample_20261115 import build, stats

def brute_chain_probability(lengths):
    n=sum(lengths)
    assert n<=8
    chain_ids=tuple(k for k,l in enumerate(lengths) for _ in range(l))
    # Permutations of labeled events: each chain's internal order is fixed.
    pred={i: tuple(j for j in range(n) if j<i and chain_ids[j]==chain_ids[i]) for i in range(n)}
    orders=[]
    for perm in permutations(range(n)):
        ranks={x:k for k,x in enumerate(perm)}
        if all(ranks[j]<ranks[i] for i,js in pred.items() for j in js):
            orders.append(perm)
    observed=Fraction(sum(chain_ids[p[0]]==chain_ids[p[1]] for p in orders), len(orders))
    exact=Fraction(sum(l*(l-1) for l in lengths),n*(n-1))
    assert observed==exact, (lengths, observed, exact)
    return len(orders), exact

for ls in [(1,1,1,1),(2,1,1),(2,2),(3,2),(3,1,1),(4,3)]:
    e,p=brute_chain_probability(ls)
    print('ENUMERATED',tuple(ls),'EXTENSIONS',e,'P2',str(p))

for k in [40,80,160,320,640,1280]:
    n,j,h,concentrated,balanced,base=build(k)
    assert sum(concentrated)==sum(balanced)==n
    assert all(sum(l>q for l in concentrated)==sum(l>q for l in balanced)==h[q] for q in range(j+1))
    _,pa,_=stats(concentrated); _,pb,_=stats(balanced)
    assert pa>pb and pa>0 and pb>0
    # Express the average deletion-weight ratio from the exact two-ideal identity.
    # H1 * rho / (H1 * rho + H0*(H0-1)) = p2
    h0,h1=h[:2]
    rho_a=Fraction(h0*(h0-1),h1)*pa/(1-pa)
    rho_b=Fraction(h0*(h0-1),h1)*pb/(1-pb)
    assert rho_a>rho_b>0
    assert Fraction(h1)*rho_a/(h1*rho_a+h0*(h0-1))==pa
    assert Fraction(h1)*rho_b/(h1*rho_b+h0*(h0-1))==pb
    print('N',n,'J',j,'H0',h0,'H1',h1,'p_high',str(pa),'p_low',str(pb),
          'rho_high/sqrtN',float(rho_a)/k,'rho_low/sqrtN',float(rho_b)/k)
print('BRUTE_FORCE_LINEAR_EXTENSION_CROSS_CHECK := PASS')
print('IDENTICAL_Hj_FOR_ALL_j_LE_J := PASS')
print('EXACT_LINEAR_EXTENSION_PROBABILITIES := PASS')
print('EXACT_RHO_IDENTITY := PASS')
print('MINKOWSKI_EXTENSION_WEIGHT_SCALING := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
