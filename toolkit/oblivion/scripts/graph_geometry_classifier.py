#!/usr/bin/env python3
import json, argparse, math

def load_adj(path):
    data=json.load(open(path))
    return data["adj"]

def ball(adj,start,R):
    seen={start}
    frontier={start}
    for _ in range(R):
        nxt=set()
        for v in frontier:
            for u in adj[v]:
                if u not in seen:
                    seen.add(u); nxt.add(u)
        frontier=nxt
    return seen

def cycle_rank(adj,verts):
    V=len(verts)
    vertset=set(verts)
    E=0
    for v in verts:
        for u in adj[v]:
            if u in vertset:
                E+=1
    E//=2
    return E-V+1

def classify(vol,cycle):
    if vol == 0:
        return "unknown"

    rho = cycle/vol

    if rho < 0.02:
        return "tree-like"

    if rho < 0.3:
        return "expander-like"

    return "2D-sheet"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph_json",required=True)
    ap.add_argument("--R",type=int,default=6)
    args=ap.parse_args()

    adj=load_adj(args.graph_json)

    verts=ball(adj,0,args.R)
    vol=len(verts)
    cyc=cycle_rank(adj,verts)

    print(json.dumps({
        "R":args.R,
        "ball_volume":vol,
        "cycle_rank":cyc,
        "ratio": cyc/vol if vol else 0,
        "classification": classify(vol,cyc)
    },indent=2))

if __name__=="__main__":
    main()
