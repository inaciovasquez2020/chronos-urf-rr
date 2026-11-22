#!/usr/bin/env python3
"""Exact stdlib-only certificate: sharp lower bound of Chronos four-event
prefix statistic under five 3-event marginals, top/bottom moments,
time reversal, and the 2-past/1-future central-event moment.
No network or repository mutations; class indices follow original poset order.
"""
from itertools import combinations, permutations, product
from collections import Counter
from fractions import Fraction as Q

def posets(n):
    pairs=list(combinations(range(n),2))
    for states in product(range(3), repeat=len(pairs)):
        e={(a,b) for (a,b),st in zip(pairs,states) if st==1}
        e|={(b,a) for (a,b),st in zip(pairs,states) if st==2}
        if all((a,c) in e for a,b in e for bb,c in e if bb==b):yield frozenset(e)

def canonical(e,n):
    return min(tuple(int((p[a],p[b]) in e) for a in range(n) for b in range(n) if a!=b)
               for p in permutations(range(n)))

def prefix(e,n):
    valid=[p for p in permutations(range(n)) if all(p.index(a)<p.index(b) for a,b in e)]
    return Q(sum((p[0],p[1]) in e for p in valid),len(valid))

def triple_type(e):
    k=len(e)
    if k==0:return 'A'
    if k==1:return 'E'
    if k==3:return 'C'
    assert k==2
    return 'V' if prefix(e,3)==1 else 'Lambda'

def triples(e):
    vals=[]
    for subset in combinations(range(4),3):
        ren={v:i for i,v in enumerate(subset)}
        vals.append(triple_type(frozenset((ren[a],ren[b]) for a,b in e if a in ren and b in ren)))
    counts=Counter(vals)
    return {k:Q(counts[k],4) for k in ('A','E','V','Lambda','C')}

def greatest(e):return int(any(all((b,a) in e for b in range(4) if b!=a) for a in range(4)))
def least(e):return int(any(all((a,b) in e for b in range(4) if b!=a) for a in range(4)))
def center(e):return int(any(sum((a,x) in e for a in range(4) if a!=x)==2 and sum((x,b) in e for b in range(4) if b!=x)==1 for x in range(4)))

four=list(posets(4))
classes={}
for e in four:
    key=canonical(e,4)
    if key not in classes: classes[key]=(e,prefix(e,4),triples(e),greatest(e),least(e))
ordered=list(classes.values())
assert len(four)==219 and len(ordered)==16
rows=[[Q(1)]*16]; rhs=[Q(1)]
q3={'A':Q(53,70),'E':Q(33,175),'V':Q(9,350),'Lambda':Q(9,350),'C':Q(1,350)}
for k in ('A','E','V','Lambda','C'):
    rows.append([v[2][k] for v in ordered]);rhs.append(q3[k])
for idx in (3,4):
    rows.append([Q(v[idx]) for v in ordered]);rhs.append(Q(1,84))
for i,(e,*_) in enumerate(ordered):
    rev=frozenset((b,a) for a,b in e)
    j=next(k for k,v in enumerate(ordered) if canonical(v[0],4)==canonical(rev,4))
    if j>i:
        row=[Q(0)]*16;row[i],row[j]=Q(1),Q(-1)
        rows.append(row);rhs.append(Q(0))
rows.append([Q(center(v[0])) for v in ordered]);rhs.append(Q(1,2940))
assert len(rows)==13
objective=[v[1] for v in ordered]
# Feasible exact rational distribution attaining the lower bound.
primal={0:Q(277,490),1:Q(66,175),5:Q(8,1225),9:Q(8,1225),11:Q(23,588),13:Q(37,7350),15:Q(1,2940)}
x=[primal.get(i,Q(0)) for i in range(16)]
assert all(a>=0 for a in x) and sum(x)==1
assert all(sum(rows[j][i]*x[i] for i in range(16))==rhs[j] for j in range(13))
lo=sum(objective[i]*x[i] for i in range(16))
assert lo==Q(157,2100)
# Exact dual lower-bound certificate: for every class i, sum_j y_j A_ji <= c_i.
y=[Q(0),Q(0),Q(1,3),Q(0),Q(0),Q(0),Q(1),Q(0),Q(-1,6),Q(-1),Q(-3,4),Q(-1),Q(0)]
assert all(sum(y[j]*rows[j][i] for j in range(13))<=objective[i] for i in range(16))
dual=sum(y[j]*rhs[j] for j in range(13))
assert dual==lo
print('FOUR_LABELED_POSETS :=',len(four))
print('UNLABELED_CLASSES :=',len(ordered))
print('EXACT_CONSTRAINT_ROWS :=',len(rows))
print('EXACT_PRIMAL_FEASIBILITY := PASS')
print('EXACT_DUAL_FEASIBILITY := PASS')
print('PRIMAL_DUAL_EQUALITY := PASS')
print('SHARP_LOWER :=',lo)
print('BOUND_SCOPE := EXACT_LISTED_MARGINALS_ONLY')
print('ACTUAL_MINKOWSKI_P_4_2 := OPEN')
print('LEAN := NOT_RUN')
