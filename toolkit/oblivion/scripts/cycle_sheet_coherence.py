#!/usr/bin/env python3
import json, argparse
from collections import deque

def load_graph(path):
    with open(path) as f:
        data=json.load(f)
    return data["adj"], data.get("meta",{})

def ball(adj,start,R):
    seen={start}
    q=deque([(start,0)])
    while q:
        v,d=q.popleft()
        if d==R: continue
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                q.append((w,d+1))
    return seen

def edge_index(adj):
    idx={}
    i=0
    for u in range(len(adj)):
        for v in adj[u]:
            if u<v:
                idx[(u,v)]=i
                i+=1
    return idx

def cycle_vectors(adj,nodes,eidx):
    S=set(nodes)
    vecs=[]
    for u in nodes:
        for v in adj[u]:
            if v in S and u<v:
                vecs.append(1<<eidx[(u,v)])
    return vecs

def rank(vecs):
    basis={}
    r=0
    for x in vecs:
        while x:
            b=x.bit_length()-1
            if b not in basis:
                basis[b]=x
                r+=1
                break
            x^=basis[b]
    return r

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph_json",required=True)
    ap.add_argument("--R",type=int,default=3)
    ap.add_argument("--limit",type=int,default=1000)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    adj,meta=load_graph(args.graph_json)
    eidx=edge_index(adj)

    inter_vecs=[]
    union_vecs=[]

    for v in range(min(len(adj),args.limit)):
        Bv=ball(adj,v,args.R)
        for w in adj[v]:
            Bw=ball(adj,w,args.R)

            inter=Bv & Bw
            union=Bv | Bw

            inter_vecs+=cycle_vectors(adj,inter,eidx)
            union_vecs+=cycle_vectors(adj,union,eidx)

    r_inter=rank(inter_vecs)
    r_union=rank(union_vecs)

    kappa=r_inter/max(r_union,1)

    out={
        "meta":{"R":args.R,"limit":args.limit},
        "intersection_rank":r_inter,
        "union_rank":r_union,
        "kappa":kappa
    }

    with open(args.out,"w") as f:
        json.dump(out,f,indent=2)

    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
