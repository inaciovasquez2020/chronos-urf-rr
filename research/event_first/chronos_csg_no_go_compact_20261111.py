#!/usr/bin/env python3
"""Exact N=2 versus N=3 projectivity audit; geometric 2+2 lower bound."""
from fractions import Fraction as F
from itertools import permutations
from math import pi
mom_s2, mom_sf = F(1,105), F(1,2100)
p3 = {'chain':6*mom_sf,'fork':3*(mom_s2-2*mom_sf),'merge':3*(mom_s2-2*mom_sf)}
p3['single']=F(3,10)-3*p3['chain']-2*(p3['fork']+p3['merge'])
p3['empty']=1-sum(p3.values())
orders={'chain':((0,1),(1,2)), 'fork':((0,2),(1,2)),
        'merge':((0,1),(0,2)), 'single':((0,1),),'empty':()}
q={}
for name,edges in orders.items():
    extensions=[p for p in permutations(range(3)) if all(p.index(a)<p.index(b) for a,b in edges)]
    q[name]=F(sum(any((p[0],p[1])==(a,b) or
          ((p[0],p[1])==(0,2) and edges==orders['chain']) for a,b in edges)
          for p in extensions),len(extensions))
assert p3=={'chain':F(1,350),'fork':F(9,350),'merge':F(9,350),
            'single':F(33,175),'empty':F(53,70)}
assert q=={'chain':1,'fork':0,'merge':1,'single':F(1,3),'empty':0},q
prefix=sum(p3[t]*q[t] for t in orders)
assert prefix==F(16,175) and F(1,10)-prefix==F(3,350)
eta=F(1,100)
centers=[(F(2,5),-F(1,5)),(F(11,20),-F(1,5)),
         (F(2,5),F(1,5)),(F(11,20),F(1,5))]
assert F(3,20)-2*eta>F(4,100)
assert F(2,5)-2*eta>F(3,20)+2*eta
assert all(min(t,1-t)>abs(x)+4*eta for t,x in centers)
box_measure=24*float((2*eta)**4)/pi
assert 0<24*box_measure**4<1
print('FRESH_N2_COMPARABILITY :=',F(1,10))
print('N3_FIRST_TWO_COMPARABILITY :=',prefix)
print('EXACT_DISCREPANCY :=',F(3,350))
print('MINKOWSKI_2PLUS2_POSITIVE_LOWER_BOUND :=',24*box_measure**4)
print('CSG_APPLICABILITY_TO_UNIFORM_EXTENSION := UNESTABLISHED')
print('ACTUAL_MINKOWSKI_PREFIX_LIMIT := OPEN')
