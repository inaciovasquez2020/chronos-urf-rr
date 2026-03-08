#!/usr/bin/env python3
import networkx as nx
import numpy as np
import argparse
import json
import random
from collections import deque

def sample_cycles(G,L,max_cycles=5000):
    cycles=set()
    nodes=list(G.nodes())
    for s in nodes:
        q=deque([(s,[s])])
        while q:
            v,path=q.popleft()
            if len(path)>L:
                continue
            for w in G.neighbors(v):
                if w==s and len(path)>=3:
                    edges=[]
                    cyc=path+[s]
                    for i in range(len(cyc)-1):
                        e=tuple(sorted((cyc[i],cyc[i+1])))
                        edges.append(e)
                    cycles.add(tuple(sorted(edges)))
                    if len(cycles)>=max_cycles:
                        return list(cycles)
                if w not in path:
                    q.append((w,path+[w]))
    return list(cycles)

def incidence_matrix(G,cycles):
    edges=list(G.edges())
    idx={tuple(sorted(e)):i for i,e in enumerate(edges)}
    M=np.zeros((len(cycles),len(edges)),dtype=np.uint8)
    for r,C in enumerate(cycles):
        for e in C:
            if e in idx:
                M[r,idx[e]]=1
    return M

def rank_f2(M):
    M=M.copy()
    rows,cols=M.shape
    r=0
    for c in range(cols):
        pivot=None
        for i in range(r,rows):
            if M[i,c]==1:
                pivot=i
                break
        if pivot is None:
            continue
        M[[r,pivot]]=M[[pivot,r]]
        for i in range(rows):
            if i!=r and M[i,c]==1:
                M[i]^=M[r]
        r+=1
        if r==rows:
            break
    return r

def run(n,d,L):
    G=nx.random_regular_graph(d,n)
    cycles=sample_cycles(G,L)
    M=incidence_matrix(G,cycles)
    r=rank_f2(M)
    return {
        "n":n,
        "cycles_sampled":len(cycles),
        "rank_F2":int(r),
        "rank_over_n":float(r/n)
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--sizes",type=int,nargs="+",default=[200,400,800,1200])
    p.add_argument("--d",type=int,default=4)
    p.add_argument("--L",type=int,default=8)
    p.add_argument("--out",default="toolkit/oblivion/results/cycle_rank_scaling.json")
    args=p.parse_args()

    results=[]
    for n in args.sizes:
        res=run(n,args.d,args.L)
        print(res)
        results.append(res)

    with open(args.out,"w") as f:
        json.dump(results,f,indent=2)

if __name__=="__main__":
    main()
