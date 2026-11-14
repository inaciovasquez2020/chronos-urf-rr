#!/usr/bin/env python3
"""Exact auditable bounds and insertion obstruction; stdlib only.
Neither evaluates the overlap moment nor proves unique Minkowski prefix limits.
"""
from fractions import Fraction as Q
from collections import defaultdict
from itertools import combinations, product
from math import factorial

# F_W(t^2) = 6t - 3t^2 -2t^3 + 6t^2 log t, t in [0,1].
# E[min(W_1,W_2)^2] = 4 int_0^1 t^3 (1-F_W(t^2))^2 dt.
# Represent polynomial with log exponent as (power_t,power_log) -> rational.
def mul(a,b):
    c=defaultdict(Q)
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            c[(i+k,j+l)] += x*y
    return c

survival={(0,0):Q(1), (1,0):Q(-6), (2,0):Q(3),
          (3,0):Q(2), (2,1):Q(-6)}
square=mul(survival,survival)
upper=Q(0)
for (p,l),a in square.items():
    # Integral t^(p+3) log(t)^l dt = (-1)^l l!/(p+4)^(l+1)
    upper += 4*a*Q((-1)**l*factorial(l),(p+4)**(l+1))
assert upper==Q(23,21168),(upper, float(upper))

# Previously proved exact mixed moments and conditional Cauchy Schwarz.
comp2=Q(1,17640)
mean_incomp=Q(3,350)
p_incomp=Q(9,10)
lower=comp2+mean_incomp**2/p_incomp
assert lower==Q(61,441000)
assert lower<upper

# Deterministic deletion identity: in every linear extension of any
# (N+1)-vertex poset, exactly n of the N+1 labels lie in the first n slots.
# Average over uniformly deleted labels, even when extension weights are nonuniform.
def extensions(pred):
    count=len(pred); out=[]
    def visit(done, rem):
        if not rem:
            out.append(tuple(done));return
        for x in sorted(rem):
            if pred[x].isdisjoint(rem):
                visit(done+[x],rem-{x})
    visit([],set(range(count)))
    return out

checks=0
pairs=list(combinations(range(4),2))
for states in product(range(3),repeat=len(pairs)):
    rel=set()
    for (i,j),v in zip(pairs,states):
        if v==1:rel.add((i,j))
        if v==2:rel.add((j,i))
    if any((i,k) not in rel for i,j in rel for jj,k in rel if jj==j): continue
    pred=[{i for i,j in rel if j==v} for v in range(4)]
    ex=extensions(pred)
    for n in (1,2,3,4):
        # Average over extensions and over deleted vertex z; exact total = n/4.
        prob=Q(sum(sum(z in L[:n] for z in range(4)) for L in ex),4*len(ex))
        assert prob==Q(n,4)
        checks+=1
assert checks==876

print('EXACT_OVERLAP_LOWER :=',lower)
print('EXACT_OVERLAP_UPPER :=',upper)
print('UPPER_DERIVATION := E[min(Wplus(X),Wplus(Y))^2]')
print('FULL_OVERLAP_MOMENT := OPEN')
print('DELETION_RANK_EXCHANGEABILITY := PASS; finite checks=',checks)
print('E[R_N,n] := n/(N+1) for N>=n in exchangeable sprinkling')
print('SUM_N E[R_N,n] := DIVERGENT for fixed n>=1')
print('PREVIOUS_INSERTION_SUMMABILITY_SUFFICIENT_CONDITION := INAPPLICABLE')
print('MINKOWSKI_PREFIX_LIMIT := OPEN')
print('LEAN_VERIFIED := NO')
