#!/usr/bin/env python3
"""Exact two-element ideal weight formula and 4D Minkowski predecessor-count moments.
Does NOT prove concentration of H0/H1 or extension-count weight ratios.
"""
from fractions import Fraction as F
from math import comb,factorial
from itertools import combinations,product
from functools import lru_cache

def extensions_count(rel,nodes):
    nodes=frozenset(nodes)
    @lru_cache(None)
    def calc(rem):
        if not rem: return 1
        return sum(calc(rem-{v}) for v in rem if not any((u,v) in rel for u in rem-{v}))
    return calc(nodes)

pairs=list(combinations(range(4),2)); testcases=0
for states in product(range(3),repeat=6):
    edges=set()
    for (a,b),v in zip(pairs,states):
        if v==1: edges.add((a,b))
        if v==2: edges.add((b,a))
    if any((a,c) not in edges for a,b in edges for bb,c in edges if b==bb):continue
    minima={i for i in range(4) if not any((j,i) in edges for j in range(4))}
    h0=len(minima)
    h1=sum(sum((i,j) in edges for i in range(4))==1 for j in range(4))
    chain,anti=[],[]
    for I in combinations(range(4),2):
        if any((j,i) in edges for i in I for j in range(4) if j not in I):continue
        w=extensions_count(frozenset(edges),frozenset(range(4))-frozenset(I))
        if (I[0],I[1]) in edges or (I[1],I[0]) in edges:chain.append(w)
        else:anti.append(w)
    assert len(chain)==h1
    assert len(anti)==comb(h0,2)
    e=extensions_count(frozenset(edges),frozenset(range(4)))
    assert sum(chain)+2*sum(anti)==e
    if chain:
        p=F(sum(chain),e)
        if anti:
            rho=F(sum(chain),len(chain))/F(sum(anti),len(anti))
            assert p == F(h1)*rho/(F(h1)*rho+h0*(h0-1))
    testcases+=1
assert testcases==219

def moment_w(n):
    # density of W_-: 3*w^(-1/2)-3*w^(1/2)+3*log(w)
    return F(6,2*n+1)-F(6,2*n+3)-F(3,(n+1)**2)

def expected_H_expand(N,j):
    return N*comb(N-1,j)*sum(((-1)**k*comb(N-1-j,k)*moment_w(j+k)
                              for k in range(N-j)),F(0))

def beta_half(a,j,N):
    # beta(j+1/2, N-j+1) = (N-j)!/[prod_{k=0}^{N-j}(j+1/2+k)]
    assert a==F(1,2)
    return F(factorial(N-j))/__import__('functools').reduce(lambda x,k:x*(F(j)+a+k),range(N-j+1),F(1))

def expected_H_beta(N,j):
    H=lambda m:sum((F(1,k) for k in range(1,m+1)),F(0))
    return 3*N*comb(N-1,j)*beta_half(F(1,2),j,N)+3*(H(j)-H(N))

nchecks=0
for N in range(1,23):
    for j in range(min(4,N)):
        a,b=expected_H_expand(N,j), expected_H_beta(N,j)
        assert a==b,(N,j,a,b)
        nchecks+=1
print('FOUR_ELEMENT_POSETS := 219 EXACT_IDEAL_EXTENSION_WEIGHT_IDENTITY PASS')
print('E_H_N_j_EXACT_FORMULA := 3*N*binom(N-1,j)*Beta(j+1/2,N-j+1) + 3*(H_j-H_N)')
print('BETA_MOMENT_TEST_CASES :=',nchecks,'PASS')
print('ASYMPTOTIC_E_H0_OVER_SQRT_N := 3*sqrt(pi)')
print('ASYMPTOTIC_E_H1_OVER_SQRT_N := (3/2)*sqrt(pi)')
print('CONDITIONAL_REQUIRED_WEIGHT_RATIO_SQRT_N := 2*sqrt(pi)/3 for p_N2 -> 1/10')
print('COUNT_CONCENTRATION := NOT_PROVED')
print('WEIGHT_RATIO_SCALING := OPEN')
print('MINKOWSKI_PREFIX_LIMIT := OPEN')
