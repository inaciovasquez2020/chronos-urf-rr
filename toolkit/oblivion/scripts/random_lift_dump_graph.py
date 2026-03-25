#!/usr/bin/env python3
import argparse, json, random

def rr_base(n, d, rng):
    stubs = []
    for v in range(n):
        stubs += [v]*d
    for _ in range(5000):
        rng.shuffle(stubs)
        adj = [set() for _ in range(n)]
        ok = True
        for i in range(0, len(stubs), 2):
            a,b = stubs[i], stubs[i+1]
            if a==b or b in adj[a]:
                ok = False
                break
            adj[a].add(b); adj[b].add(a)
        if ok:
            return adj
    raise RuntimeError("base rr failed")

def theta_base():
    adj = [set() for _ in range(6)]
    def add(u,v):
        adj[u].add(v); adj[v].add(u)
    add(0,2); add(2,1)
    add(0,3); add(3,1)
    add(0,4); add(4,5); add(5,1)
    return adj

def cycle_base(m):
    adj = [set() for _ in range(m)]
    for i in range(m):
        adj[i].add((i-1)%m); adj[i].add((i+1)%m)
    return adj

def random_lift(base_adj, n_fiber, rng):
    B = len(base_adj)
    N = B*n_fiber
    adj = [set() for _ in range(N)]
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", choices=["theta","cycle","rr"], default="rr")
    ap.add_argument("--base_n", type=int, default=30)
    ap.add_argument("--base_d", type=int, default=3)
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--fiber", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    if args.base == "theta":
        base = theta_base()
    elif args.base == "cycle":
        base = cycle_base(args.m)
    else:
        base = rr_base(args.base_n, args.base_d, rng)

    G = random_lift(base, args.fiber, rng)
    payload = {
        "meta": {
            "base": args.base, "base_n": args.base_n, "base_d": args.base_d, "m": args.m,
            "fiber": args.fiber, "seed": args.seed, "N": len(G)
        },
        "adj": [sorted(list(s)) for s in G]
    }
    with open(args.out, "w") as f:
        json.dump(payload, f)
    print(args.out)

if __name__ == "__main__":
    main()
