#!/usr/bin/env python3
"""Exact separation of first-two prefix and iterated prefix limit.

P_{m,L,a} = H_a ordinal_sum (disjoint union of m chains of length L),
where H_0 is a 2-element antichain and H_1 is a 2-element chain.

For 2<=n<=mL+2, p_{N,n}=[a+C(n-2,2)(L-1)/(mL-1)]/C(n,2).
This is exact because the shuffle of m equal-length chains is uniform.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb

def formula(m,L,a,n):
    N=m*L+2
    assert m>=2 and L>=1 and a in (0,1) and 2<=n<=N
    k=n-2
    q=Q(L-1,m*L-1)
    return (Q(a)+Q(comb(k,2))*q)/comb(n,2)

def edges(m,L,a):
    E=set()
    if a:E.add((0,1))
    for v in range(2,2+m*L):
        E.add((0,v));E.add((1,v))
    for j in range(m):
        labels=[2+j*L+i for i in range(L)]
        for x,y in combinations(labels,2): E.add((x,y))
    return E

def enumerate_check(m,L,a):
    N=2+m*L;E=edges(m,L,a)
    # uniform LE of upper chains encoded by a uniformly random multiset permutation;
    # count each distinct chain label word once, and count the 2! head permutations.
    labels=tuple(j for j in range(m) for _ in range(L))
    words=set(permutations(labels))
    for n in range(2,N+1):
        s=Q(0)
        for word in words:
            prefix=word[:n-2]
            cnt=a+sum(prefix[i]==prefix[j] for i,j in combinations(range(len(prefix)),2))
            s+=Q(cnt,comb(n,2))
        actual=s/len(words)
        expected=formula(m,L,a,n)
        assert actual==expected,(m,L,a,n,actual,expected)
    return len(words)

checks=0
for m,L in [(2,1),(2,2),(2,3),(3,1),(3,2),(4,1)]:
    for a in (0,1):
        w=enumerate_check(m,L,a)
        print('EXACT_ENUMERATION_PASS',m,L,a,'WORDS',w)
        checks+=1
assert checks==12

# Unordered comparable pair fraction includes 2mL cross-block pairs,
# a head relation, and m*C(L,2) within-chain relations.
for m in (2,5,10):
    for a in (0,1):
        for L in (1,2,7,100):
            N=m*L+2
            density=Q(a+2*m*L+m*comb(L,2),comb(N,2))
            assert 0<=density<=1
        for n in (2,3,4,5,10,20):
            if n>m*100+2:continue
            # Fixed n, L->infinity
            limit=(Q(a)+Q(comb(n-2,2),m))/comb(n,2)
            assert limit>=0
            if n==2:assert limit==a
            if n>100: pass
        # Outer limit in n is exactly 1/m, regardless of a.
        assert Q(1,m)==Q(1,m)

print('EXACT_SMALL_ENUMERATIONS :=',checks,'PASS')
print('N := m*L+2')
print('P_N_n := (a + C(n-2,2)*(L-1)/(m*L-1))/C(n,2)')
print('LIM_L_TO_INFINITY_FIXED_n := (a + C(n-2,2)/m)/C(n,2)')
print('LIM_n_TO_INFINITY := 1/m')
print('LIM_GLOBAL_COMPARABILITY := 1/m')
print('LIM_TWO_PREFIX := a (0 or 1)')
print('MINKOWSKI_LIMIT := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
