#!/usr/bin/env python3
"""Bounded exact verification of the replica sampling-transfer inequality."""
from fractions import Fraction as F
from itertools import permutations, combinations
from math import comb

def poset(n, edge_mask):
    pred=[0]*n;bit=0
    for j in range(n):
        for i in range(j):
            if edge_mask>>bit&1:pred[j]|=1<<i
            bit+=1
    for j in range(n):
        for i in range(j):
            if pred[j]>>i&1:pred[j]|=pred[i]
    return pred

def extensions(pred):
    n=len(pred);out=[]
    def go(seq,mask):
        if len(seq)==n:out.append(tuple(seq));return
        for v in range(n):
            if not(mask>>v&1) and (pred[v]&~mask)==0:
                go(seq+(v,),mask|(1<<v))
    go((),0)
    return out

def signature(pred,points):
    # Canonical complete induced order: invariant under all relabelings.
    return min(tuple(int(bool(pred[p[j]]>>p[i]&1))
                     for j in range(len(p)) for i in range(len(p)) if i!=j)
               for p in permutations(points))

def profile(pred,A,k):
    counts={}
    for pts in combinations(sorted(A),k):
        s=signature(pred,pts)
        counts[s]=counts.get(s,0)+1
    return {s:F(v,comb(len(A),k)) for s,v in counts.items()}

def test(pred,A,B,k):
    assert len(A)==len(B)
    n=len(A);r=len(set(A)-set(B))
    pa=profile(pred,A,k);pb=profile(pred,B,k)
    tv=sum(abs(pa.get(s,0)-pb.get(s,0)) for s in pa.keys()|pb.keys())/2
    match=F(comb(n-r,k),comb(n,k)) if n-r>=k else F(0)
    assert tv<=1-match<=F(k*r,n)
    return tv

def main():
    count=0
    for n in range(2,6):
        for edge_mask in range(1<<comb(n,2)):
            pred=poset(n,edge_mask)
            for prefix_size in range(2,n+1):
                prefixes=sorted({tuple(sorted(e[:prefix_size])) for e in extensions(pred)})
                for A in prefixes:
                    for B in prefixes:
                        for k in range(1,min(3,prefix_size)+1):
                            test(pred,A,B,k);count+=1
    assert count==56088, count
    print("EXACT_PAIRWISE_TESTS := 56088")
    print("REPLICA_SAMPLING_TRANSFER := PASS")
    print("MINKOWSKI_SAMPLING_LIMIT := OPEN")
if __name__=="__main__":main()
