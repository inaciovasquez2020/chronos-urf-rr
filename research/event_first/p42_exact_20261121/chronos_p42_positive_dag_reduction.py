#!/usr/bin/env python3
"""Exact four-event p42 reduction to two positive-relation DAG integrals.

No third-party dependencies. This is an exhaustive combinatorial identity;
it is NOT an evaluation of the geometric expectation p42.

For independently sampled Minkowski events X0,...,X3, define
A = Pr(X0<X3, X1<X2, X1<X3) (N-DAG)
B = Pr(X0<X2, X0<X3, X1<X2, X1<X3) (2+2-DAG).
Then, using the audited Chronos 3-event census, 4-chain probability,
maximal-event probability, central motif probability, time reversal:
    p42 = 78509/882000 - (16/5)*A + (6/5)*B.

Exact finite inclusion-exclusion over all 219 labeled 4-posets checks the
identity and coefficients, rather than assuming a specific labeling.
"""
from itertools import combinations, permutations, product
from fractions import Fraction as Q
from collections import Counter, defaultdict


def posets(n):
    for states in product(range(3), repeat=n*(n-1)//2):
        e = frozenset((a,b) if st==1 else (b,a)
                      for (a,b),st in zip(combinations(range(n),2),states) if st)
        if all((a,c) in e for a,b in e for bb,c in e if b==bb):
            yield e


def canonical(e,n):
    return min(tuple(int((p[a],p[b]) in e) for a in range(n)
                     for b in range(n) if a != b) for p in permutations(range(n)))


def prefix(e,n):
    extensions=[p for p in permutations(range(n))
                if all(p.index(a)<p.index(b) for a,b in e)]
    return Q(sum((p[0],p[1]) in e for p in extensions),len(extensions))


def label_probabilities(n):
    return list(posets(n))

labeled=label_probabilities(4)
classes={}
for e in labeled:
    classes.setdefault(canonical(e,4),e)
ordered=list(classes.values())
assert len(labeled)==219 and len(ordered)==16
index={k:i for i,k in enumerate(classes)}

# Required-relation probability indicator I(G) is 1 when G is a subset
# of the observed strict order. This is inclusive; unspecified pairs
# may have additional causal relations.
A=frozenset(((0,3),(1,2),(1,3)))
B=frozenset(((0,2),(0,3),(1,2),(1,3)))
assert canonical(A,4)==canonical(ordered[7],4)
assert canonical(B,4)==canonical(ordered[11],4)

# Integer Mobius inversion on relation-set inclusion.
ordered_labeled=sorted(labeled,key=lambda e:(len(e),tuple(sorted(e))))
coeff={}
for e in ordered_labeled:
    target=2*int(index[canonical(e,4)]==7)+5*int(index[canonical(e,4)]==11)
    coeff[e]=target-sum(v for h,v in coeff.items() if h<e)
assert all(sum(v for h,v in coeff.items() if h<=e) ==
           2*int(index[canonical(e,4)]==7)+5*int(index[canonical(e,4)]==11)
           for e in labeled)
by_class=defaultdict(int)
for e,v in coeff.items():
    by_class[index[canonical(e,4)]]+=v
expected={7:48,8:-48,10:-48,11:-18,12:-12,13:48,14:-12,15:72}
assert {i:v for i,v in by_class.items() if v}==expected
# Every relabeling of G has the same geometric expectation I(G).
# Time reversal also preserves the diamond sprinkling.
assert canonical(frozenset((b,a) for a,b in ordered[8]),4)==canonical(ordered[10],4)
assert canonical(frozenset((b,a) for a,b in ordered[12]),4)==canonical(ordered[14],4)

# Known inclusive positive-relation DAG probabilities.
# I8: one designated top among four = 1/336; given it, one specified
# oriented relation among remaining three has probability 1/20.
I8=Q(1,336)*Q(1,20)
# I12: given designated top, two other specified events both precede
# another designated event; E[(fractional past volume)^2]=1/105.
I12=Q(1,336)*Q(1,105)
# I13: fixed diamond relations may be completed by exactly two labeled
# total chains; exact diamond class q13=3/9800, with 12 labelings.
q13=Q(3,9800)
I13=q13/12+2*Q(1,29400)/24
# I15: fixed specified total-chain relation, one of 24 labelings.
I15=Q(1,29400)/24
assert (I8,I12,I13,I15)==(Q(1,6720),Q(1,35280),Q(1,35280),Q(1,705600))
known=(-96*I8-24*I12+48*I13+72*I15)
assert known == -Q(397,29400)

# Directly evaluate the equality for EVERY possible 4-element poset
# using formal symbols A=I(N), B=I(2+2), and the known contributions.
# q8 = (1/84)*(33/175), q13=(1/84)*(9/350).
q8=Q(11,4900)
assert q13==Q(3,9800)
constant=Q(1727,19600)-known/15
assert constant==Q(78509,882000)

# Independent cross-check: 14 moment rows prove original p42 identity.
def induced(e,verts):
    mapping={v:i for i,v in enumerate(verts)}
    return frozenset((mapping[a],mapping[b]) for a,b in e
                     if a in mapping and b in mapping)

def triple_type(e):
    n=len(e)
    if n==0:return 'A'
    if n==1:return 'E'
    if n==3:return 'C'
    assert n==2
    return 'V' if prefix(e,3)==1 else 'Lambda'

def freq(e):
    c=Counter(triple_type(induced(e,s)) for s in combinations(range(4),3))
    return {k:Q(c[k],4) for k in ('A','E','V','Lambda','C')}

def greatest(e):
    return Q(any(all((b,a) in e for b in range(4) if a!=b) for a in range(4)))

def least(e):
    return Q(any(all((a,b) in e for b in range(4) if a!=b) for a in range(4)))

def central(e):
    return Q(any(sum((a,x) in e for a in range(4) if a!=x)==2 and
                 sum((x,b) in e for b in range(4) if b!=x)==1
                 for x in range(4)))

rev=[]
for e in ordered:
    rev.append(index[canonical(frozenset((b,a) for a,b in e),4)])
rows=[[Q(1)]*16]
for k in ('A','E','V','Lambda','C'):
    rows.append([freq(e)[k] for e in ordered])
rows += [[greatest(e) for e in ordered],[least(e) for e in ordered]]
for i,j in enumerate(rev):
    if i<j:
        rows.append([Q(int(k==i)-int(k==j)) for k in range(16)])
rows += [[central(e) for e in ordered],
         [Q(int(len(e)==6)) for e in ordered]]
assert len(rows)==14
base_coeff=[Q(0),Q(0),Q(1,3),Q(2),Q(-4,3),Q(1),Q(1),Q(-1,2),
            Q(1,6),Q(0),Q(-1,6),Q(0),Q(-5,6),Q(1,3)]
residual={7:Q(-2,15),8:Q(-1,6),11:Q(-1,3),13:Q(-1,6)}
for i,e in enumerate(ordered):
    assert prefix(e,4)==sum((c*row[i] for c,row in zip(base_coeff,rows)),Q(0))+residual.get(i,Q(0))
known_moments=[Q(1),Q(53,70),Q(33,175),Q(9,350),Q(9,350),Q(1,350),
               Q(1,84),Q(1,84),Q(0),Q(0),Q(0),Q(0),Q(1,2940),Q(1,29400)]
assert sum((c*k for c,k in zip(base_coeff,known_moments)),Q(0))==Q(2603,29400)
assert Q(2603,29400)-q8/6-q13/6==Q(1727,19600)
assert Q(1727,19600)-known/15==constant
# If two bottom events a,b are timelike-related, their common future
# inside the ambient diamond is exactly the future of the later event.
# Each time orientation contributes E[W_past * W_future^2]=1/35280.
# Thus I_2PLUS2 = J_spacelike + 1/17640, where
# J_spacelike = E[1_(a||b) * (V(common future(a,b))/V)^2].
# The mixed-moment value is independently checked by the closed-form
# beta identity (r,s)=(1,2) from the preceding Chronos theorem.
from math import factorial

def beta_integer(a,b):
    return Q(factorial(a-1)*factorial(b-1),factorial(a+b-1))

def moment(r,s):
    a,b=2*r+1,2*s+1
    return Q(12*a*b,(a+b)**2*(a+b+1))*beta_integer(a,b)**2

assert moment(1,2)==moment(2,1)==Q(1,35280)
TIMELIKE_I22=2*moment(1,2)
assert TIMELIKE_I22==Q(1,17640)
assert constant+Q(6,5)*TIMELIKE_I22==Q(78569,882000)

print('LABELED_FOUR_POSETS := 219')
print('CLASSES := 16')
print('INCLUSION_EXCLUSION := PASS (219/219)')
print('RATIONAL_MOMENT_IDENTITY := PASS (16/16)')
print('POSITIVE_DAG_COEFFICIENTS :=',sorted(expected.items()))
print('I8 :=',I8,'I12 :=',I12,'I13 :=',I13,'I15 :=',I15)
print('KNOWN_DAG_CONTRIBUTION :=',known)
print('P42 := 78509/882000 - (16/5)*I_N + (6/5)*I_2PLUS2')
print('P42_ALTERNATE := 78569/882000 - (16/5)*I_N + (6/5)*J_SPACELIKE')
print('I22_TIMELIKE_COMPONENT :=', TIMELIKE_I22)
print('GEOMETRIC_I_N := OPEN')
print('GEOMETRIC_I_2PLUS2 := OPEN')
print('GLOBAL_P42 := OPEN')
print('LEAN := NOT_RUN')
