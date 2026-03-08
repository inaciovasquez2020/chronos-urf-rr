#!/usr/bin/env python3
import networkx as nx
import itertools
import numpy as np
import argparse

def cycles_upto_length(G, L):
    cycles=set()
    for v in G.nodes():
        for path in nx.simple_cycles(nx.DiGraph(G)):
            if len(path)<=L:
                edges=set()
                for i in range(len(path)):
                    u=path[i]
                    w=path[(i+1)%len(path)]
                    edges.add(tuple(sorted((u,w))))
                cycles.add(tuple(sorted(edges)))
    return list(cycles)

def incidence_matrix(G, cycles):
    edges=list(G.edges())
    index={tuple(sorted(e)):i for i,e in enumerate(edges)}
    M=np.zeros((len(cycles),len(edges)),dtype=int)
    for r,C in enumerate(cycles):
        for e in C:
            M[r,index[e]]=1
    return M

def rank_f2(M):
    M=M.copy()%2
    r=0
    for c in range(M.shape[1]):
        pivot=None
        for i in range(r,M.shape[0]):
            if M[i,c]==1:
                pivot=i
                break
        if pivot is None:
            continue
        M[[r,pivot]]=M[[pivot,r]]
        for i in range(M.shape[0]):
            if i!=r and M[i,c]==1:
                M[i]^=M[r]
        r+=1
    return r

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--n",type=int,default=200)
    p.add_argument("--d",type=int,default=4)
    p.add_argument("--L",type=int,default=8)
    args=p.parse_args()

    G=nx.random_regular_graph(args.d,args.n)

    cycles=cycles_upto_length(G,args.L)
    M=incidence_matrix(G,cycles)
    r=rank_f2(M)

    print("n:",args.n)
    print("cycles:",len(cycles))
    print("rank_F2:",r)
    print("rank/n:",r/args.n)

if __name__=="__main__":
    main()
