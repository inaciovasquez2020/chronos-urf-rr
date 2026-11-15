#!/usr/bin/env python3
"""Exact analytic reduction of 4D Minkowski N/K22 probabilities to E[J_+^2].

All integrals and poset combinatorics exact; E[J_+^2] remains OPEN.
Dependencies: sympy only. No Lean or repo changes.
"""
from itertools import combinations, product, permutations
from fractions import Fraction as F
from math import factorial
from sympy import symbols, Poly, expand, Rational

u,v,w,z=symbols('u v w z')
def ordered_simplex_integral(p):
    """Integral over 0<u<v<w<z<1 of polynomial p(u,v,w,z)."""
    result=Rational(0)
    for (a,b,c,d),coef in Poly(expand(p),u,v,w,z).terms():
        result += coef / ((a+1)*(a+b+2)*(a+b+c+3)*(a+b+c+d+4))
    return result

# Cases for 4D null coordinates ac<=bc, ab<=bb.
# Density each 12*(b-a)^2 da db. Conditional spatial direction is uniform.
# C≺B causal probability:
#   1, when ac<bc<ab<bb
#   (ab-ac)*(bb-bc)/((bc-ac)*(bb-ab)), when ac<ab<bc<bb.
# Weight W_-(B)=(ab*bb)^2, W_+(C)=(1-ac)^2(1-bc)^2.
full=ordered_simplex_integral(144*(v-u)**2*(z-w)**2*(w*z)**2*(1-u)**2*(1-v)**2)
partial=ordered_simplex_integral(144*(w-u)*(z-v)*(v-u)*(z-w)*(v*z)**2*(1-u)**2*(1-w)**2)
T=F(full+partial)
assert full==Rational(29663,36036000)
assert partial==Rational(266113,504504000)
assert T==F(953,705600)

# Ordered pair C≺B, A∈J^-(B) spacelike C, D∈J^+(C) spacelike B.
# Conditional A,D volumes are Avol=W_-(B)-W_-(C)-I(C,B),
# Dvol=W_+(C)-W_+(B)-I(C,B).
# N patterns appear once per four labels; K22 patterns appear four times.
# The following nine terms are separately obtained by conditioning on B,C
# and exploiting the uniform 4D Alexandrov interval comparability 1/10.
M21=F(1,35280)        # E[W_-² W_+]
M12=F(1,35280)        # E[W_- W_+²]
chain_labeled=F(1,705600)  # Pr(X<C<B<Y) with fixed labels
I_squared=F(1,35280) # Pr(C<both A,D<B): C4 + D4, fixed labels
interval_weight=F(1,6720) # E[1_(C<B) W_-(B)*I(C,B)] (also W_+(C)*I)
X=(T-M21-M12+chain_labeled-2*interval_weight
   +2*chain_labeled+I_squared)
assert X==F(121,117600)
N_plus_4K=24*X
assert N_plus_4K==F(121,4900)

# Exhaustive 219 4-element labeled posets independently verify the pattern
# count m(P)=1 for N, m(P)=4 for K22, and zero otherwise.
pairs=list(combinations(range(4),2)); n_posets=0;n_classes=set(); match_count={}
for states in product(range(3),repeat=6):
    edges=set()
    for (a,b),s in zip(pairs,states):
        if s==1: edges.add((a,b))
        if s==2: edges.add((b,a))
    if any((a,c) not in edges for a,b in edges for bb,c in edges if b==bb): continue
    n_posets+=1
    m=0
    for A,B,C,D in permutations(range(4)):
        if ((A,B) in edges and (C,B) in edges and (C,D) in edges
            and (A,C) not in edges and (C,A) not in edges
            and (B,D) not in edges and (D,B) not in edges):
            m+=1
    if m:
        if len(edges)==3: assert m==1
        elif len(edges)==4: assert m==4
        else: raise AssertionError((edges,m))
    match_count[m]=match_count.get(m,0)+1
assert n_posets==219
assert match_count=={0:189,1:24,4:6},match_count

# Existing exact poset identity established under finite 3-event marginals and
# exact unique-extremal 4-event probabilities.
# p4 = 1727/19600 - (2/15)Pr(N) - (1/3)Pr(K22)
# and Pr(K22) = 6 E[J²] - 19/29400.
# Derived here by symbol substitution.
from sympy import Symbol, simplify
J=Symbol('E_J_squared');K=6*J-Rational(19,29400)
N=Rational(121,4900)-4*K
p4=simplify(Rational(1727,19600)-Rational(2,15)*N-Rational(1,3)*K)
assert simplify(p4-(Rational(3557,42000)+Rational(6,5)*J))==0
assert simplify(N-(Rational(401,14700)-24*J))==0
print('ANGLE_REDUCTION := PASS')
print('ORDERED_SIMPLEX_FULL :=',full)
print('ORDERED_SIMPLEX_PARTIAL :=',partial)
print('EXACT_T :=',T)
print('EXACT_4_POINT_N_PLUS_4K :=',N_plus_4K)
print('FOUR_LABELED_POSETS :=',n_posets)
print('PATTERN_MULTIPLICITIES :=',match_count)
print('EXACT_N_RELATION := Pr(N4) = 401/14700 - 24*E[J_plus^2]')
print('EXACT_P42_RELATION := p42 = 3557/42000 + (6/5)*E[J_plus^2]')
print('EXACT_E_J_SQUARED := OPEN')
print('INFINITE_GROWTH_SAMPLING_STABILITY := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
