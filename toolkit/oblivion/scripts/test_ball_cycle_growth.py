#!/usr/bin/env python3
import argparse
import json
import random
from collections import deque

def random_d_regular(n, d, seed):
    rng = random.Random(seed)
    if n * d % 2 != 0:
        raise ValueError("n*d must be even")
    for _ in range(200):
        stubs = [v for v in range(n) for _ in range(d)]
        rng.shuffle(stubs)
        adj = [set() for _ in range(n)]
        ok = True
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i+1]
            if u == v or v in adj[u]:
                ok = False
                break
            adj[u].add(v)
            adj[v].add(u)
        if ok and all(len(adj[v]) == d for v in range(n)):
            return [sorted(list(x)) for x in adj]
    raise RuntimeError("failed to generate graph")

def ball_vertices(adj, root, R):
    seen = {root}
    q = deque([(root,0)])
    while q:
        u,d = q.popleft()
        if d == R:
            continue
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append((v,d+1))
    return sorted(seen)

def induced_edges(adj, verts):
    s=set(verts)
    edges=[]
    for u in verts:
        for v in adj[u]:
            if u < v and v in s:
                edges.append((u,v))
    return edges

def beta1(adj, root, R):
    verts = ball_vertices(adj, root, R)
    edges = induced_edges(adj, verts)
    idx = {v:i for i,v in enumerate(verts)}
    seen=set()
    comps=0
    for v in verts:
        if v in seen:
            continue
        comps+=1
        q=[v]
        seen.add(v)
        while q:
            u=q.pop()
            for w in adj[u]:
                if w in idx and w not in seen:
                    seen.add(w)
                    q.append(w)
    return len(edges)-len(verts)+comps

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=800)
    ap.add_argument("--d", type=int, default=4)
    ap.add_argument("--Rmax", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    adj = random_d_regular(args.n, args.d, args.seed)

    rows=[]
    for R in range(1,args.Rmax+1):
        vals=[]
        for v in range(min(200,args.n)):
            vals.append(beta1(adj,v,R))
        rows.append({
            "R":R,
            "avg_beta1": sum(vals)/len(vals),
            "max_beta1": max(vals),
            "min_beta1": min(vals)
        })

    out={"meta":{"n":args.n,"d":args.d},"rows":rows}

    with open(args.out,"w") as f:
        json.dump(out,f,indent=2)

    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
