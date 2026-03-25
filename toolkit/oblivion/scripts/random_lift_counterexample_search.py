#!/usr/bin/env python3
import argparse, json, random, time
from collections import defaultdict, deque

def cycle_basis_rank_mod2(adj):
    # rank of cycle space: m - n + c (over F2)
    n = len(adj)
    m2 = sum(len(adj[v]) for v in range(n))
    m = m2 // 2
    # count components
    seen = [False]*n
    c = 0
    for s in range(n):
        if not seen[s]:
            c += 1
            dq = deque([s]); seen[s]=True
            while dq:
                u=dq.popleft()
                for w in adj[u]:
                    if not seen[w]:
                        seen[w]=True
                        dq.append(w)
    return m - n + c

def induced_ball(adj, root, R):
    vis = {root: 0}
    q = deque([root])
    while q:
        u = q.popleft()
        if vis[u] == R: 
            continue
        for w in adj[u]:
            if w not in vis:
                vis[w] = vis[u] + 1
                q.append(w)
    nodes = sorted(vis.keys())
    idx = {v:i for i,v in enumerate(nodes)}
    sub = [set() for _ in nodes]
    for v in nodes:
        for w in adj[v]:
            if w in idx:
                sub[idx[v]].add(idx[w])
    return sub, nodes

def local_cycle_span_proxy(adj, R):
    # proxy: max cycle-rank among balls + count distinct ball cycle-ranks (cheap invariant)
    n = len(adj)
    ranks = []
    for v in range(n):
        sub,_ = induced_ball(adj,v,R)
        ranks.append(cycle_basis_rank_mod2(sub))
    return {
        "max_ball_cycle_rank": max(ranks) if ranks else 0,
        "min_ball_cycle_rank": min(ranks) if ranks else 0,
        "distinct_ball_cycle_ranks": len(set(ranks)),
        "avg_ball_cycle_rank": (sum(ranks)/len(ranks)) if ranks else 0.0,
    }

def random_lift(base_adj, n_fiber, seed=0):
    # random n_fiber-lift of a base graph: each base edge gets random permutation on fiber
    rng = random.Random(seed)
    B = len(base_adj)
    # label lifted vertices as (b,i) -> b*n_fiber + i
    N = B*n_fiber
    adj = [set() for _ in range(N)]
    # process each undirected base edge once (u<v)
    for u in range(B):
        for v in base_adj[u]:
            if u < v:
                perm = list(range(n_fiber))
                rng.shuffle(perm)
                for i in range(n_fiber):
                    a = u*n_fiber + i
                    b = v*n_fiber + perm[i]
                    adj[a].add(b); adj[b].add(a)
    return adj

def base_cycle_graph(m):
    # cycle C_m
    adj = [set() for _ in range(m)]
    for i in range(m):
        adj[i].add((i-1)%m)
        adj[i].add((i+1)%m)
    return adj

def base_theta():
    # theta graph: two vertices joined by three internally-disjoint length-2 paths (6 vertices total)
    # vertices: 0=A,1=B, paths: A-2-B, A-3-B, A-4-5-B (one length-3)
    adj = [set() for _ in range(6)]
    def add(u,v):
        adj[u].add(v); adj[v].add(u)
    add(0,2); add(2,1)
    add(0,3); add(3,1)
    add(0,4); add(4,5); add(5,1)
    return adj

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", choices=["cycle","theta"], default="theta")
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--fiber", type=int, default=200)
    ap.add_argument("--R", type=int, default=2)
    ap.add_argument("--trials", type=int, default=50)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="toolkit/oblivion/results/random_lift_counterexample_scan.json")
    args = ap.parse_args()

    if args.base == "cycle":
        base = base_cycle_graph(args.m)
    else:
        base = base_theta()

    results = []
    t0 = time.time()
    for t in range(args.trials):
        s = args.seed + t
        G = random_lift(base, args.fiber, seed=s)
        inv = local_cycle_span_proxy(G, args.R)
        inv.update({"trial": t, "seed": s, "N": len(G), "base": args.base, "R": args.R, "fiber": args.fiber})
        results.append(inv)

    payload = {
        "meta": {
            "base": args.base, "m": args.m, "fiber": args.fiber, "R": args.R,
            "trials": args.trials, "seed0": args.seed, "seconds": time.time()-t0
        },
        "results": results
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload["meta"], indent=2))
    # print top candidates: high max_ball_cycle_rank but low distinct_ball_cycle_ranks (homogeneity proxy)
    cand = sorted(results, key=lambda x: (x["distinct_ball_cycle_ranks"], -x["max_ball_cycle_rank"]))[:10]
    print("top_candidates:")
    for r in cand:
        print({k:r[k] for k in ["trial","seed","max_ball_cycle_rank","distinct_ball_cycle_ranks","avg_ball_cycle_rank"]})

if __name__ == "__main__":
    main()
