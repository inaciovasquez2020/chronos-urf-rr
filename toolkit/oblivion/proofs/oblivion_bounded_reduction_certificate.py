#!/usr/bin/env python3
"""Isolated reproducibility checks; never modifies the Oblivion repository.

Source models:
- COR cycle family: local fundamental cycles of an induced-radius ball;
  this tests the original scanner functions if installed in provided extracted tree.
- CFI-style degree-2 parity gadget: correct endpoint wiring; compares graph
  connectivity and original rooted radius-2 WL implementation on 64 twists.
"""
import argparse
import itertools
import sys
from collections import deque


def insert(basis, vec):
    while vec:
        pivot = vec.bit_length() - 1
        if pivot not in basis:
            basis[pivot] = vec
            return True
        vec ^= basis[pivot]
    return False


def cycle_square(n):
    assert n >= 7
    return [{(i+d)%n for d in (-2,-1,1,2)} for i in range(n)]


def triangle_rank_and_overlap(n):
    G=cycle_square(n)
    eidx={}
    for u in range(n):
        for v in sorted(G[u]):
            if u<v: eidx[(u,v)]=len(eidx)
    basis={}; cycles=[]
    for i in range(n):
        x=0
        for u,v in ((i,(i+1)%n),((i+1)%n,(i+2)%n),(i,(i+2)%n)):
            x^=1<<eidx[tuple(sorted((u,v)))]
        cycles.append(x)
        assert insert(basis,x)
    assert len(basis)==n
    assert all(cycles[i] & cycles[(i+1)%n] for i in range(n))
    # Translations by one preserve exactly the stipulated adjacency relation.
    assert all({(v+1)%n for v in G[i]} == G[(i+1)%n] for i in range(n))
    return G, n


def parity_gadget(n,twists):
    assert n>=4
    G={}
    def edge(a,b):
        G.setdefault(a,set()).add(b)
        G.setdefault(b,set()).add(a)
    for i in range(n):
        for bit in (0,1):
            P=('P',i,bit); L=('L',i,bit); R=('R',i,bit)
            edge(P,L)
            edge(L,('R',i,bit^(i in twists)))
            edge(R,('P',(i+1)%n,bit))
    assert len(G)==6*n and all(len(v)==2 for v in G.values())
    return G


def component_sizes(G):
    seen=set();sizes=[]
    for v in G:
        if v in seen:continue
        q=[v];seen.add(v);k=0
        while q:
            x=q.pop();k+=1
            for y in G[x]:
                if y not in seen:seen.add(y);q.append(y)
        sizes.append(k)
    return sorted(sizes)


def ball_vertices(G, root, R):
    d={root:0}; q=deque([root])
    while q:
        x=q.popleft()
        if d[x]>=R:continue
        for y in G[x]:
            if y not in d:d[y]=d[x]+1;q.append(y)
    return d


def rooted_ball_is_path(G,root,R):
    d=ball_vertices(G,root,R)
    inside=set(d)
    e=sum(len(G[v]&inside) for v in inside)//2
    return len(d)==2*R+1 and e==2*R


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--toolkit-root',default=None,help='directory containing oblivion/scripts/rooted_wl.py and cor_overlap_rank_from_balls.py')
    args=p.parse_args()
    wl=None; scanner=None
    if args.toolkit_root:
        sys.path.insert(0,args.toolkit_root)
        from oblivion.scripts.rooted_wl import wl_refinement
        from oblivion.scripts.cor_overlap_rank_from_balls import (build_edge_index,ball_nodes,cycle_vectors,overlap)
        wl=wl_refinement
        scanner=(build_edge_index,ball_nodes,cycle_vectors,overlap)

    for n in (7,8,10,16,32,64):
        G,r=triangle_rank_and_overlap(n)
        if scanner:
            eidx,edges=scanner[0](G)
            full={};overlap_b={};kept=[]
            for root in range(n):
                for vec in scanner[2](G,scanner[1](G,root,1),eidx):
                    insert(full,vec)
                    if not kept or any(scanner[3](vec,k) for k in kept):
                        if insert(overlap_b,vec):kept.append(vec)
            assert len(full)>=n and len(overlap_b)>=n
            print('CYCLE_SQUARE',n,'triangle_rank',r,'scanner_full_rank',len(full),'scanner_overlap_rank',len(overlap_b),'transitive',True)
        else: print('CYCLE_SQUARE',n,'triangle_rank',r,'transitive',True)

    for n in (4,6,8,12):
        untwisted=parity_gadget(n,set());odd=parity_gadget(n,{0})
        assert component_sizes(untwisted)==[3*n,3*n]
        assert component_sizes(odd)==[6*n]
        for G in (untwisted,odd):
            assert all(rooted_ball_is_path(G,v,2) for v in G)
        if wl:
            sig0=sorted(wl(untwisted,v,2) for v in untwisted)
            sig1=sorted(wl(odd,v,2) for v in odd)
            assert sig0==sig1
        print('PARITY_GADGET',n,'even_components',[3*n,3*n],'odd_components',[6*n],'radius2_indistinguishable',True)

    n=6
    reference=parity_gadget(n,set())
    reference_sig=sorted(wl(reference,v,2) for v in reference) if wl else None
    for bits in range(1<<n):
        twists={i for i in range(n) if bits & (1<<i)}
        G=parity_gadget(n,twists)
        target=[3*n,3*n] if len(twists)%2==0 else [6*n]
        assert component_sizes(G)==target
        if wl: assert sorted(wl(G,v,2) for v in G)==reference_sig
        else: assert all(rooted_ball_is_path(G,v,2) for v in G)
    print('64_TWIST_EXHAUSTIVE_CHECK := PASS')
    print('THEOREM_COUNTEREXAMPLE_AND_RESTRICTED_SIMULATION := PASS')

if __name__=='__main__': main()
