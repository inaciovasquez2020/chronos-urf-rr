#!/usr/bin/env python3
import argparse
import json
import math
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
            u, v = stubs[i], stubs[i + 1]
            if u == v or v in adj[u]:
                ok = False
                break
            adj[u].add(v)
            adj[v].add(u)
        if ok and all(len(adj[v]) == d for v in range(n)):
            return [sorted(list(x)) for x in adj]
    raise RuntimeError("failed to generate simple d-regular graph")

def ball_vertices(adj, root, R):
    seen = {root}
    q = deque([(root, 0)])
    while q:
        u, dist = q.popleft()
        if dist == R:
            continue
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append((v, dist + 1))
    return sorted(seen)

def induced_edges(adj, verts):
    s = set(verts)
    edges = []
    for u in verts:
        for v in adj[u]:
            if u < v and v in s:
                edges.append((u, v))
    return edges

def beta1_ball(adj, root, R):
    verts = ball_vertices(adj, root, R)
    edges = induced_edges(adj, verts)
    idx = {v: i for i, v in enumerate(verts)}
    seen = set()
    comps = 0
    for v in verts:
        if v in seen:
            continue
        comps += 1
        q = deque([v])
        seen.add(v)
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w in idx and w not in seen:
                    seen.add(w)
                    q.append(w)
    return len(edges) - len(verts) + comps

def rooted_ball_signature(adj, root, R):
    verts = ball_vertices(adj, root, R)
    local = {v: i for i, v in enumerate(verts)}
    edges = []
    for u in verts:
        for v in adj[u]:
            if v in local and local[u] < local[v]:
                edges.append((local[u], local[v]))
    degs = tuple(sorted(sum(1 for a, b in edges if a == i or b == i) for i in range(len(verts))))
    return {
        "nverts": len(verts),
        "nedges": len(edges),
        "degs": degs,
        "beta1": beta1_ball(adj, root, R),
    }

def corr_quotient(adj, R):
    types = {}
    for v in range(len(adj)):
        sig = rooted_ball_signature(adj, v, R)
        key = json.dumps(sig, sort_keys=True)
        types[key] = sig["beta1"]
    corr = sum(b * b for b in types.values())
    return corr, len(types)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--d", type=int, default=4)
    ap.add_argument("--R", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = []
    for s in range(args.seeds):
        adj = random_d_regular(args.n, args.d, s)
        corr, ntypes = corr_quotient(adj, args.R)
        rows.append({
            "seed": s,
            "n": args.n,
            "d": args.d,
            "R": args.R,
            "corr": corr,
            "types": ntypes,
            "log_n": math.log(max(args.n, 2)),
        })

    out = {
        "meta": {
            "n": args.n,
            "d": args.d,
            "R": args.R,
            "seeds": args.seeds,
            "invariant": "quotient_CORR_proxy",
        },
        "rows": rows,
        "summary": {
            "min_corr": min(r["corr"] for r in rows),
            "max_corr": max(r["corr"] for r in rows),
            "avg_corr": sum(r["corr"] for r in rows) / len(rows),
            "min_types": min(r["types"] for r in rows),
            "max_types": max(r["types"] for r in rows),
        },
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
