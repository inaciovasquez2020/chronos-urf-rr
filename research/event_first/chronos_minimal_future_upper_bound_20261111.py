#!/usr/bin/env python3
"""Exhaustive finite-poset certificate for first-birth strict-future upper bound."""
from functools import lru_cache

def check_all():
    total=0
    for n in range(2,7):
        full=(1<<n)-1
        configurations=0; checks=0
        for bits in range(1<<(n*(n-1)//2)):
            p=[0]*n; t=0
            for j in range(n):
                for i in range(j):
                    if bits>>t&1:p[j]|=1<<i
                    t+=1
            for j in range(n):
                for i in range(j):
                    if p[j]>>i&1:p[j]|=p[i]
            @lru_cache(None)
            def extensions(mask):
                if mask==full:return 1
                return sum(extensions(mask|(1<<i)) for i in range(n)
                           if not (mask>>i&1) and p[i]&~mask==0)
            denominator=extensions(0)
            for x in range(n):
                if p[x]:continue
                size=1+sum(bool(p[y]>>x&1) for y in range(n))
                assert n*extensions(1<<x)<=size*denominator,(n,bits,x,size)
                checks+=1
            configurations+=1
        total+=checks
        print('N=',n,'FORWARD_EDGE_CONFIGURATIONS=',configurations,
              'MINIMAL_EVENT_BOUNDS_CHECKED=',checks,flush=True)
    assert total==66633,total
    print('TOTAL_MINIMAL_EVENT_CHECKS :=',total)
    print('FIRST_BIRTH_UPPER_BOUND := PASS')
    print('FOUR_DIMENSIONAL_SELECTION_ASYMPTOTICS := OPEN')

if __name__=='__main__':check_all()
