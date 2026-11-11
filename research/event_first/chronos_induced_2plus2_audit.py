#!/usr/bin/env python3
"""Read-only exact 2+2 obstruction certificate. Python >=3.8 stdlib only.
No geometry numerical tolerances: all causal inequalities checked over Q.
Enumerates natural-label directed graph configurations through n=5.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb

EPS=Q(1,22)
centers=((Q(-1,8),Q(-1,2),Q(0),Q(0)),
         (Q(1,8),Q(-1,2),Q(0),Q(0)),
         (Q(-1,8),Q(1,2),Q(0),Q(0)),
         (Q(1,8),Q(1,2),Q(0),Q(0)))
# cubes center +/- 1/64; center sequence a1 b1 a2 b2.
# sufficient squared interval checks for EVERY point inside cubes.
# same-worldline: dt_min=1/4-2eps, spatial_dist_sq_max=3*(2eps)^2
assert (Q(1,4)-2*EPS)**2 > 3*(2*EPS)**2
# cross-worldline: dt_max=1/4+2eps, x_dist_min=1-2eps
assert (Q(1)-2*EPS)**2 > (Q(1,4)+2*EPS)**2
# within each t-slice, spatial x separation at least 1-2eps, dt at most 2eps
assert (1-2*EPS)**2 > (2*EPS)**2
# inside |t|+sqrt(x*x+y*y+z*z)<1 via rational conservative sqrt bound r<=|x|+|y|+|z|
assert Q(1,8)+EPS+Q(1,2)+3*EPS < 1


def bitrows(n, mask):
    edges=[(i,j) for i in range(n) for j in range(i+1,n)]
    a=[0]*n
    for k,(i,j) in enumerate(edges):
        if mask>>k & 1: a[i] |= 1<<j
    for i in range(n-1,-1,-1):
        for j in range(i+1,n):
            if a[i]>>j & 1: a[i] |= a[j]
    return a

def induced_2plus2_bipartitions(rows,n):
    count=0
    for four in combinations(range(n),4):
        rel=[(i,j) for i,j in combinations(four,2) if rows[i]>>j & 1]
        if len(rel)==2 and len(set(rel[0]+rel[1]))==4:
            count+=1
    return count

def induced_2plus2_edge_exhaustive(rows,n):
    count=0
    for four in combinations(range(n),4):
        arcs={(a,b) for a in four for b in four if a<b and rows[a]>>b&1}
        if len(arcs)!=2: continue
        indeg={x:0 for x in four}; outdeg={x:0 for x in four}
        for a,b in arcs: indeg[b]+=1;outdeg[a]+=1
        if sorted(indeg.values())==[0,0,1,1] and sorted(outdeg.values())==[0,0,1,1] and all(indeg[x]*outdeg[x]==0 for x in four):
            count+=1
    return count

for n in (4,5):
    edges=comb(n,2); p=Q(2,5)
    exact=Q(0); positive=0
    for mask in range(1<<edges):
        rows=bitrows(n,mask)
        a=induced_2plus2_bipartitions(rows,n)
        b=induced_2plus2_edge_exhaustive(rows,n)
        assert a==b
        positive+=(a>0)
        exact+=p**mask.bit_count()*(1-p)**(edges-mask.bit_count())*Q(a,comb(n,4))
    print(f'N={n} EDGES={edges} CONFIGURATIONS={1<<edges} WITH_2PLUS2={positive} EXPECTED_DENSITY={exact}')

# Four disjoint spacetime cubes of side 1/11 inside D, uniform volume sampling.
# q = (1/11)^4 / (2*pi/3) = 3/(2*pi*11^4)
# probability of one event in each cube = 24*q^4.
# For a finite iid sample, expected density of induced 2+2 >=delta.
# For any target semiorder, one edited pair destroys at most C(N-2,2) forbidden 4-subsets.
# Thus #pair_edits/C(N,2) >= observed 2+2 density/6.
print('GEOMETRIC_WITNESS := PASS (all inequalities exact)')
print('FOUR_CUBE_EVENT_PROBABILITY_LOWER_BOUND := 24*(3/(2*pi*11**4))**4')
print('SEM IORDER_EDIT_DISTANCE_BOUND := induced_2plus2_density/6'.replace('SEM I','SEMI'))
print('LEAN_VERIFICATION := NOT_RUN; REPOSITORY_EDITS := NONE')