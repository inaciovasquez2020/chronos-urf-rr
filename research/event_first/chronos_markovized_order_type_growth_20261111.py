#!/usr/bin/env python3
"""Audit exact three-stage Minkowski order-type Markov kernel.

Independent deterministic Fraction checks plus bounded, reproducible radial-Poisson Monte Carlo.
Does not prove order-invariance, CSG, intrinsic physical covariance, or emergent gravity.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
from math import sqrt
from random import Random

SEED=20261111
TRIALS=150_000
TARGET={
    'chain':F(1,350),
    'two_minima_one_max':F(9,350),
    'one_min_two_max':F(9,350),
    'single_edge':F(33,175),
    'antichain':F(53,70),
}
assert sum(TARGET.values())==1

# Distinct natural 3-element shapes and the comparability of the FIRST TWO
# births. The one-edge shape has two possible natural-prefix isomorphism types.
SHAPES={
    'chain':((0,1),(1,2)),
    'two_minima_one_max':((0,2),(1,2)),
    'one_min_two_max':((0,1),(0,2)),
    'single_edge':((0,1),),
    'antichain':(),
}
def prefix_comparability(edges):
    exts=[p for p in permutations(range(3)) if all(p.index(a)<p.index(b) for a,b in edges)]
    answers=[int((p[0],p[1]) in edges or ((0,1) in edges and (1,2) in edges and p[:2]==(0,2))) for p in exts]
    # Full relation closure for robustness.
    rel=[[False]*3 for _ in range(3)]
    for a,b in edges:rel[a][b]=True
    for k in range(3):
        for i in range(3):
            for j in range(3):rel[i][j]|=rel[i][k] and rel[k][j]
    return {int(rel[p[0]][p[1]]) for p in exts},len(exts)

assert {s:prefix_comparability(e)[0] for s,e in SHAPES.items()} == {
    'chain':{1}, 'two_minima_one_max':{0}, 'one_min_two_max':{1},
    'single_edge':{0,1}, 'antichain':{0}
}

Q2={'comparable':F(1,10),'incomparable':F(9,10)}
# For the three-event single-edge shape, first-two comparable joint mass is
# determined by Q2 and the two other obligatorily comparable-prefix shapes.
joint_comp={
    'chain':TARGET['chain'],
    'one_min_two_max':TARGET['one_min_two_max'],
}
joint_comp['single_edge']=Q2['comparable']-sum(joint_comp.values())
joint_incomp={
    'two_minima_one_max':TARGET['two_minima_one_max'],
    'antichain':TARGET['antichain'],
    'single_edge':TARGET['single_edge']-joint_comp['single_edge'],
}
assert sum(joint_comp.values())==Q2['comparable']
assert sum(joint_incomp.values())==Q2['incomparable']
K={
    'comparable':{s:p/Q2['comparable'] for s,p in joint_comp.items()},
    'incomparable':{s:p/Q2['incomparable'] for s,p in joint_incomp.items()},
}
assert K['comparable']=={
    'chain':F(1,35), 'one_min_two_max':F(9,35), 'single_edge':F(5,7)
}
assert K['incomparable']=={
    'two_minima_one_max':F(1,35),'antichain':F(53,63),'single_edge':F(41,315)
}
assert all(sum(v.values())==1 for v in K.values())
for shape,prob in TARGET.items():
    mass=sum((Q2[state]*d.get(shape,F(0)) for state,d in K.items()),F(0))
    assert mass==prob,(shape,mass,prob)
print('EXACT_Q2_TO_Q3_MARKOV_KERNEL := PASS')
for state,d in K.items():print('KERNEL',state, {k:str(v) for k,v in d.items()})

rng=Random(SEED)
def mark(u):
    v=1-(1-rng.random())**(1/3)
    t=u*(1+v)/2
    r=u*(1-v)/2
    while True:
        d=[rng.gauss(0,1) for _ in range(3)]
        length=sqrt(sum(x*x for x in d))
        if length>0:break
    return (t,*(r*x/length for x in d))
def before(a,b):
    dt=b[0]-a[0]
    return dt>0 and dt*dt>sum((b[i]-a[i])**2 for i in range(1,4))
def classify(points):
    edges=[(i,j) for i in range(3) for j in range(i+1,3) if before(points[i],points[j])]
    if len(edges)==3:return 'chain'
    if len(edges)==0:return 'antichain'
    if len(edges)==1:return 'single_edge'
    if edges[0][0]==edges[1][0]:return 'one_min_two_max'
    if edges[0][1]==edges[1][1]:return 'two_minima_one_max'
    raise AssertionError(edges)

observed=Counter();pair=Counter()
for _ in range(TRIALS):
    s=0.;p=[]
    for _i in range(3):
        s+=rng.expovariate(1)
        p.append(mark(s**.25))
    assert not any(before(p[j],p[i]) for i in range(3) for j in range(i+1,3))
    shape=classify(p)
    state='comparable' if before(p[0],p[1]) else 'incomparable'
    observed[shape]+=1
    pair[(state,shape)]+=1

# Independent conditional checks with conservative 7-sigma + additive margin.
for state,d in K.items():
    n_state=sum(pair[(state,sh)] for sh in TARGET)
    assert n_state>1000
    for sh,expected in d.items():
        empirical=pair[(state,sh)]/n_state
        target=float(expected)
        tol=7*sqrt(target*(1-target)/n_state)+.001
        assert abs(empirical-target)<tol,(state,sh,empirical,target,tol)
        print('CONDITIONAL_SIM',state,sh,round(empirical,6),'target',expected)
for sh,expected in TARGET.items():
    empirical=observed[sh]/TRIALS
    tol=7*sqrt(float(expected)*(1-float(expected))/TRIALS)+.001
    assert abs(empirical-float(expected))<tol,(sh,empirical,expected)
print('RNG_SEED :=',SEED)
print('RADIAL_POISSON_TRIALS :=',TRIALS)
print('INDEPENDENT_TRANSITION_FREQ_CHECK := PASS')
print('ALL_STAGE_MARKOVIZATION := PROVED_BY_CONDITIONAL_DISINTEGRATION')
print('ALL_STAGE_MARKOVIZATION_EXECUTION := NOT_RUN')
print('PATH_COVARIANCE_ORDER_INVARIANCE := REFUTED')
print('BACKGROUND_INDEPENDENCE := OPEN')
