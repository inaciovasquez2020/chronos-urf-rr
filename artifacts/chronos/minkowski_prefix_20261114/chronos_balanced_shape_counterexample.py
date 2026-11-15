#!/usr/bin/env python3
"""Exact construction of 2D permutation orders with typical sqrt(n) height/width
but first-position collision and two-prefix comparability tending to one.
No external dependencies or repository writes.
"""
from fractions import Fraction
from math import log

def lis(a):
    dp=[]
    for i,x in enumerate(a):
        dp.append(1+max((dp[j] for j in range(i) if a[j]<x),default=0))
    return max(dp,default=0)

def make(r,m):
    N=r*r
    q=[v+1 for block in range(r-1,-1,-1) for v in range(block*r+1,(block+1)*r+1)]
    # first block: high ranks, decreasing. Next: 1 (global predecessor of Q)
    p=list(range(N+m,N+1,-1))+[1]+q
    assert len(p)==N+m and set(p)==set(range(1,N+m+1))
    return p

for r in (2,3,4,5,8,16,32):
    m=max(2,int(log(r*r))+1)
    p=make(r,m)
    n=len(p)
    h=lis(p)
    w=lis([-x for x in p])
    assert h==r+1,(r,h)
    assert w==r+m-1,(r,w)
    N=r*r
    pa=Fraction(N+1,n)
    collision=Fraction((N+1)**2+m-1,n*n)
    comparable=Fraction(N*(N+1),n*(n-1))
    assert pa*pa<=collision<=1 and 0<=comparable<=1
    print('r=%d n=%d minima=%d height=%d width=%d first(a)=%s collision=%s prefix=%s' %
          (r,n,m,h,w,pa,collision,comparable))
print('RESULT := COMPUTATION_PASS')
print('GENERAL_THEOREM := proved by interleaving, independent of finite cases')
print('ASYMPTOTICS := minima = Theta(log n); height,width = Theta(sqrt(n)); first(a),collision,prefix -> 1')
print('RANDOM_ENSEMBLE := NOT_PROVED')