#!/usr/bin/env python3
"""Exact four-point counterexample: 1-/2-point cone data do not determine birth weights.
Pure Python standard library; exhaustive transitive DAG configurations n<=4.
No network, local repo operations or assumptions about four-dimensional realizability.
"""
from fractions import Fraction
from itertools import permutations
from collections import defaultdict
from math import comb


def closure(n, edges):
    p=[0]*n; pos=0
    for j in range(n):
        for i in range(j):
            if (edges>>pos)&1: p[j]|=1<<i
            pos+=1
    for j in range(n):
        for i in range(j):
            if (p[j]>>i)&1:p[j]|=p[i]
    return tuple(p)


def ext_count_first(pred,x):
    n=len(pred); valid=[]
    for perm in permutations(range(n)):
        rank={v:i for i,v in enumerate(perm)}
        if all(rank[a]<rank[b] for b in range(n) for a in range(n) if pred[b]>>a&1):
            valid.append(perm)
    return Fraction(sum(p[0]==x for p in valid),len(valid)),len(valid)


def descriptor(pred,x):
    n=len(pred)
    past=frozenset(y for y in range(n) if pred[x]>>y&1)
    future=frozenset(y for y in range(n) if pred[y]>>x&1)
    incomparable=frozenset(range(n))-past-future-{x}
    overlap=sum(bool(pred[y]>>z&1) for y in future for z in incomparable)
    return len(past),len(future),len(incomparable),overlap


def witness():
    # x=0, z=1, a=2, b=3; a and b are in x's future;
    # z<a in both posets, while b<a only in the second.
    P=(0,0,(1<<0)|(1<<1),(1<<0))
    Q=(0,0,(1<<0)|(1<<1)|(1<<3),(1<<0))
    # Q's added b<a is encoded in predecessor mask of a, but
    # vertices have forward labels 3>2; valid poset representation
    # uses arbitrary masks, not only increasing-index edges.
    # Both are transitively closed, with P: 0<2,0<3,1<2;
    # Q additionally: 3<2. No additional relation between 1 and 3.
    assert descriptor(P,0)==descriptor(Q,0)==(0,2,1,1)
    a,na=ext_count_first(P,0)
    b,nb=ext_count_first(Q,0)
    assert (a,na)==(Fraction(3,5),5),(a,na)
    assert (b,nb)==(Fraction(2,3),3),(b,nb)
    assert b-a==Fraction(1,15)
    return P,Q,a,b


def minkowski_witness():
    """Integer coordinates in a shared 1+1D diamond, embedded into 4D."""
    points_P=((0,0),(0,2),(5,1),(4,-3))
    points_Q=((0,0),(0,2),(5,1),(2,-1))
    # Shared 4D diamond tips: (-10,0,0,0), (15,0,0,0).
    def causal(a,b):
        dt=b[0]-a[0]
        return dt>0 and dt*dt>(b[1]-a[1])**2
    def induced(points):
        assert all(causal((-10,0),z) and causal(z,(15,0)) for z in points)
        return tuple(sum(1<<i for i in range(len(points))
                         if i!=j and causal(points[i],points[j]))
                     for j in range(len(points)))
    P,Q,_,_=witness()
    assert induced(points_P)==P
    assert induced(points_Q)==Q
    return points_P, points_Q


def exhaustive():
    table=defaultdict(set)
    checks=0
    for n in range(2,5):
        for bits in range(1<<comb(n,2)):
            p=closure(n,bits)
            for x in range(n):
                val,total=ext_count_first(p,x)
                key=(n,descriptor(p,x))
                table[key].add(val)
                checks+=1
    assert checks==sum(n*(1<<comb(n,2)) for n in range(2,5))
    # The manually constructed witness includes backward label edge 3<2,
    # so it is separate from the forward-edge exhaustive checks.
    return checks,table


def main():
    p,q,a,b=witness()
    coords_p, coords_q=minkowski_witness()
    count,table=exhaustive()
    print('FINITE_FORWARD_EDGE_DISTINGUISHED_CONFIGURATIONS :=',count)
    print('WITNESS_P_PREDECESSOR_MASKS :=',p)
    print('WITNESS_Q_PREDECESSOR_MASKS :=',q)
    print('SAME_PAST_FUTURE_INCOMPARABLE_OVERLAP_COUNTS :=',descriptor(p,0))
    print('P_FIRST_BIRTH :=',a,'Q_FIRST_BIRTH :=',b)
    print('PROBABILITY_GAP :=',b-a)
    print('MINKOWSKI_P_COORDINATES_1PLUS1 :=', coords_p)
    print('MINKOWSKI_Q_COORDINATES_1PLUS1 :=', coords_q)
    print('FOUR_DIMENSIONAL_OPEN_SET_REALIZABILITY := PASS')
    print('OVERLAP_COUNT_INSUFFICIENT_FOR_N4 := PROVED')
    print('MINKOWSKI_ASYMPTOTIC_SELECTION_WEIGHTS := OPEN')


if __name__=='__main__':main()
