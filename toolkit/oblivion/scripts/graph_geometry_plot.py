#!/usr/bin/env python3
import json, argparse, math
import matplotlib.pyplot as plt

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
                    seen.add(u)
                    nxt.add(u)
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
    return max(E-V+1,0)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph_json",required=True)
    ap.add_argument("--max_R",type=int,default=10)
    ap.add_argument("--out",default="geometry_plot.png")
    args=ap.parse_args()

    adj=load_adj(args.graph_json)

    Rs=[]
    volumes=[]
    cycles=[]
    ratios=[]

    for R in range(1,args.max_R+1):
        verts=ball(adj,0,R)
        vol=len(verts)
        cyc=cycle_rank(adj,verts)

        Rs.append(R)
        volumes.append(vol)
        cycles.append(cyc)
        ratios.append(cyc/vol if vol else 0)

    plt.figure(figsize=(10,6))
    plt.plot(Rs,volumes,label="|B_R| (volume)")
    plt.plot(Rs,cycles,label="β₁(B_R) (cycle rank)")
    plt.plot(Rs,ratios,label="ρ = β₁/|B_R|")

    plt.xlabel("R")
    plt.title("Local Geometry Signature")
    plt.legend()
    plt.grid(True)

    plt.savefig(args.out)
    print("saved:",args.out)

if __name__=="__main__":
    main()
