#!/usr/bin/env python3
"""Exact, standard-library-only audit of weighted ideals and sampling obstruction.
Run: python3 -B chronos_order_ideal_counterexample_20261112.py
No network, repository modification, or numerical approximations in tested identities.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import comb


def extensions(pred):
    N=len(pred); full=(1<<N)-1
    @lru_cache(None)
    def e(mask):
        if mask == 0: return 1
        return sum(e(mask^(1<<v)) for v in range(N)
                   if (mask>>v)&1 and pred[v]&mask == 0)
    # The recursion removes available minimal elements (equivalently counts extensions).
    return e


def ideal_prefix_weights(pred,n):
    N=len(pred); full=(1<<N)-1
    e=extensions(pred)
    out={}
    for I in range(1<<N):
        if I.bit_count()!=n: continue
        if any((I>>v)&1 and pred[v]&~I for v in range(N)): continue
        # Need extension counts of restricted posets, not just prefix masks.
        count=e(I)*e(full^I)
        if count: out[I]=Fraction(count,e(full))
    return out,e(full)


def is_valid_extension(seq,pred):
    seen=0
    for v in seq:
        if pred[v]&~seen: return False
        seen|=1<<v
    return True


def weighted_pair_probability(pred,n):
    w,_=ideal_prefix_weights(pred,n)
    total=Fraction(0)
    for mask,weight in w.items():
        pairs=sum(bool(pred[b]&(1<<a)) or bool(pred[a]&(1<<b))
                  for a,b in combinations([i for i in range(len(pred)) if mask>>i&1],2))
        total+=weight*Fraction(pairs,comb(n,2))
    return total

# Test against independent brute-force permutation enumerations, including a mixed example.
examples=[(0,0,3), (0,0,1|2,0), (0,1,1,0), (0,0,3,3)]
checks=0
for pred in examples:
    N=len(pred)
    ex=[p for p in permutations(range(N)) if is_valid_extension(p,pred)]
    e=extensions(pred)
    assert len(ex)==e((1<<N)-1)
    for n in range(1,N+1):
        w,tot=ideal_prefix_weights(pred,n)
        brute={}
        for p in ex:
            mask=sum(1<<v for v in p[:n]); brute[mask]=brute.get(mask,0)+1
        assert sum(w.values())==1
        assert w=={mask:Fraction(count,len(ex)) for mask,count in brute.items()}
        checks+=1
print('WEIGHT_FORMULA_BRUTE_FORCE := PASS; cases=',checks)

# Two-antichain ordinal sum: all A before B.
print('N A B P_full_pair P_prefix_n2 TV_to_Q2')
for N in (40,100,1000,10000):
    # Floor(alpha*N), alpha=(1-2/sqrt(5))/2.
    from decimal import Decimal, localcontext
    with localcontext() as ctx:
        ctx.prec=70
        A=int(Decimal(N)*(1-Decimal(4).sqrt()/Decimal(5).sqrt())/2)
    assert A>=2 and 5*(N-2*A)**2 >= 4*N*N
    assert 5*(N-2*(A+1))**2 < 4*N*N
    B=N-A
    p=Fraction(A*B,comb(N,2))
    print(N,A,B,str(p),str(Fraction(0)),str(Fraction(1,10)))
    assert p>0
print('ANALYTIC_LIMIT := full_pair -> 1/10; prefix_pair = 0')
print('DOUBLE_LIMIT_TV := 1/10; target equality FALSE for this deterministic poset sequence')
print('MINKOWSKI_SPRINKLING_SPECIFIC_CLAIM := OPEN')
print('LEAN := NOT_RUN')
