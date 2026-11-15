#!/usr/bin/env python3
"""Independent standard-library exact audit of four-point Minkowski interval-volume inputs.

Proof scope: exact polynomial integrals and a finite-poset multiplicity check.
No claim to evaluate the full common-future second moment or infinite-growth law.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb

# Null-coordinate measure for a point: 12(b-a)^2 da db on 0<a<b<1.
def mixed_moment(r,s):
    total=F()
    for i in range(2*s+1):
        for j in range(2*s+1):
            for k, c in enumerate((1,-2,1)):
                total+=F(12*(-1)**(i+j)*comb(2*s,i)*comb(2*s,j)*c,
                         (2*r+i+k+1)*(4*r+i+j+4))
    return total

assert mixed_moment(0,0)==1
assert mixed_moment(1,0)==mixed_moment(0,1)==F(1,20)
assert mixed_moment(2,0)==mixed_moment(0,2)==F(1,105)
assert mixed_moment(3,0)==mixed_moment(0,3)==F(1,336)
assert mixed_moment(1,1)==F(1,2100)
assert mixed_moment(2,1)==mixed_moment(1,2)==F(1,35280)

# Conditioning on B: past(B) is a copy of the standard diamond.  Conditional
# C uniform in past(B), its relative future volume inside past(B) has first
# and second moments M_(0,1) and M_(0,2).
interval_linear=mixed_moment(3,0)*mixed_moment(0,1)
interval_square=mixed_moment(3,0)*mixed_moment(0,2)
assert interval_linear==F(1,6720)
assert interval_square==F(1,35280)

# Independent exact four-simplex integration: sparse polynomial arithmetic in
# ordered variables u<v<w<z (indexes 0,1,2,3).  This does not call sympy.
ZERO=(0,0,0,0)
def lin(*terms):
    out={}
    for coefficient,index in terms:
        key=ZERO if index is None else tuple(int(j==index) for j in range(4))
        out[key]=out.get(key,F())+F(coefficient)
    return {k:v for k,v in out.items() if v}
def multiply(*polynomials):
    acc={ZERO:F(1)}
    for polynomial in polynomials:
        nxt={}
        for a,x in acc.items():
            for b,y in polynomial.items():
                k=tuple(a[i]+b[i] for i in range(4))
                nxt[k]=nxt.get(k,F())+x*y
        acc={k:v for k,v in nxt.items() if v}
    return acc
def pw(polynomial,n): return multiply(*([polynomial]*n))
def smplx(polynomial):
    return sum((F(c,(a+1)*(a+b+2)*(a+b+d+3)*(a+b+d+e+4))
                for (a,b,d,e),c in polynomial.items()),F())

u,v,w,z=(lin((1,i)) for i in range(4))
def dif(p,q):
    neg={k:-coef for k,coef in q.items()}
    out=p.copy()
    for k,c in neg.items():out[k]=out.get(k,F())+c
    return out
one=lin((1,None))

# Region 1 ac=u<bc=v<ab=w<bb=z, both center directions automatically causal.
full=multiply(lin((144,None)),pw(dif(v,u),2),pw(dif(z,w),2),pw(w,2),pw(z,2),pw(dif(one,u),2),pw(dif(one,v),2))
# Region 2 ac=u<ab=v<bc=w<bb=z, angular causality fraction
# (v-u)(z-w)/((w-u)(z-v)) ? Careful: physical null-coordinate formula is
# f=(ab-ac)(bb-bc)/((bc-ac)(bb-ab)), = (v-u)(z-w)/((w-u)(z-v)).
# The Radon density 144(w-u)^2(z-v)^2 cancels denominators, leaving
# 144(w-u)(z-v)(v-u)(z-w).
partial=multiply(lin((144,None)),dif(w,u),dif(z,v),dif(v,u),dif(z,w),pw(v,2),pw(z,2),pw(dif(one,u),2),pw(dif(one,w),2))
Tf=smplx(full);Tp=smplx(partial);T=Tf+Tp
assert Tf==F(29663,36036000),(Tf,'full')
assert Tp==F(266113,504504000),(Tp,'partial')
assert T==F(953,705600)

# Four-chain probability with all four labels in fixed temporal order.
# Given the top event B, the other three must form a fixed labeled 3-chain
# inside past(B). That conditional probability equals M_(1,1)=1/2100.
fixed_chain=mixed_moment(3,0)*mixed_moment(1,1)
assert fixed_chain==F(1,705600)
# Product expansion of A= Wpast(B)-Wpast(C)-I and
# B= Wfuture(C)-Wfuture(B)-I:
X=(T-2*mixed_moment(2,1)+3*fixed_chain
   -2*interval_linear+interval_square)
assert X==F(121,117600)
assert 24*X==F(121,4900)

# Verify all labeled N4/K22 pattern multiplicities without geometry.
counts={}
for state in product(range(3),repeat=6):
    E=set()
    for (a,b),orientation in zip(combinations(range(4),2),state):
        if orientation==1:E.add((a,b))
        if orientation==2:E.add((b,a))
    if any((a,c) not in E for a,b in E for bb,c in E if b==bb):continue
    hits=0
    for A,B,C,D in permutations(range(4)):
        hits+=((A,B) in E and (C,B) in E and (C,D) in E
              and (A,C) not in E and (C,A) not in E
              and (B,D) not in E and (D,B) not in E)
    counts[hits]=counts.get(hits,0)+1
assert counts=={0:189,1:24,4:6},counts

print('MOMENT_M30 :=',mixed_moment(3,0))
print('E[1_C<B Wpast(B) I(C,B)] :=',interval_linear)
print('E[1_C<B Wfuture(C) I(C,B)] :=',interval_linear,'by time reversal')
print('E[1_C<B I(C,B)^2] :=',interval_square)
print('ORDERED_SIMPLEX_T_FULL :=',Tf)
print('ORDERED_SIMPLEX_T_PARTIAL :=',Tp)
print('T :=',T)
print('PATTERN_MULTIPLICITY_COUNTS :=',counts)
print('P(N4)+4 P(K22) :=',24*X)
print('RESULT := EXACT_RATIONAL_PASS')
print('MINKOWSKI_E[J_plus^2] := OPEN')
print('MINKOWSKI_INFINITE_GROWTH_STABILITY := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
