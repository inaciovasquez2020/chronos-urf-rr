#!/usr/bin/env python3
import json, argparse
from collections import deque

def load_graph(path):
    with open(path) as f:
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

def parity_cycles(adj,nodes):
    S=set(nodes)
    vec=[]
    for u in nodes:
        for v in adj[u]:
            if v in S and u<v:
                vec.append((u+v)%2)
    return vec

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph_json",required=True)
    ap.add_argument("--R",type=int,default=3)
    ap.add_argument("--limit",type=int,default=1000)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    adj=load_graph(args.graph_json)

    parity_sum=0
    for v in range(min(len(adj),args.limit)):
        nodes=ball(adj,v,args.R)
        cycles=parity_cycles(adj,nodes)
        parity_sum+=sum(cycles)

    out={"parity_signal":parity_sum}

    with open(args.out,"w") as f:
        json.dump(out,f,indent=2)

    print(out)

if __name__=="__main__":
    main()
