#!/usr/bin/env python3
import networkx as nx
import json
import argparse
import random

def bfs_ball(G, root, R):
    seen={root}
    frontier=[root]
    for _ in range(R):
        nxt=[]
        for v in frontier:
            for u in G.neighbors(v):
                if u not in seen:
                    seen.add(u)
                    nxt.append(u)
        frontier=nxt
    return seen

def sample_cycles(G,L,samples=4000):
    cycles=[]
    nodes=list(G.nodes())
    for _ in range(samples):
        v=random.choice(nodes)
        path=[v]
        visited={v}
        cur=v
        for _ in range(L):
            nbrs=list(G.neighbors(cur))
            if not nbrs:
                break
            nxt=random.choice(nbrs)
            if nxt in visited:
                idx=path.index(nxt)
                cyc=tuple(path[idx:])
                if len(cyc)>=3:
                    cycles.append(cyc)
                break
            path.append(nxt)
            visited.add(nxt)
            cur=nxt
    return cycles

def cycle_signature(G,cycle):
    return tuple(sorted(G.degree(v) for v in cycle))

def run(n,d,R,L):
    G=nx.random_regular_graph(d,n,seed=11)
    root=0
    ball=bfs_ball(G,root,R)
    H=G.subgraph(ball).copy()

    cycles=sample_cycles(H,L)

    sigs=set()
    for c in cycles:
        sigs.add(cycle_signature(H,c))

    return {
        "n":n,
        "ball_size":len(H),
        "cycles_sampled":len(cycles),
        "distinct_cycle_signatures":len(sigs)
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sizes",nargs="+",type=int,default=[200,400,800])
    ap.add_argument("--d",type=int,default=4)
    ap.add_argument("--R",type=int,default=4)
    ap.add_argument("--L",type=int,default=8)
    ap.add_argument("--out",type=str,required=True)
    args=ap.parse_args()

    res=[]
    for n in args.sizes:
        r=run(n,args.d,args.R,args.L)
        print(r)
        res.append(r)

    with open(args.out,"w") as f:
        json.dump(res,f,indent=2)

if __name__=="__main__":
    main()
