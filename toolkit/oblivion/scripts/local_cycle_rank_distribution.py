#!/usr/bin/env python3
import json, argparse
from collections import deque

def load_graph(p):
    with open(p) as f:
        d=json.load(f)
    return d["adj"]

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

def cycle_rank(adj,nodes):
    S=set(nodes)
    edges=0
    for u in nodes:
        for v in adj[u]:
            if v in S:
                edges+=1
    edges//=2
    verts=len(nodes)

    seen=set()
    comp=0
    for v in nodes:
        if v in seen: continue
        comp+=1
        q=[v]
        seen.add(v)
        while q:
            x=q.pop()
            for y in adj[x]:
                if y in S and y not in seen:
                    seen.add(y)
                    q.append(y)
    return edges-verts+comp

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph_json",required=True)
    ap.add_argument("--R",type=int,default=3)
    ap.add_argument("--limit",type=int,default=1000)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    adj=load_graph(args.graph_json)

    ranks=[]
    for v in range(min(len(adj),args.limit)):
        nodes=ball(adj,v,args.R)
        ranks.append(cycle_rank(adj,nodes))

    out={
        "min":min(ranks),
        "max":max(ranks),
        "avg":sum(ranks)/len(ranks)
    }

    with open(args.out,"w") as f:
        json.dump(out,f,indent=2)

    print(out)

if __name__=="__main__":
    main()
