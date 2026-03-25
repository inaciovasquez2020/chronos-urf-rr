#!/usr/bin/env python3
import argparse, json, random

def random_regular_graph(n, d, seed=0):
    rng = random.Random(seed)
    stubs = []
    for v in range(n):
        stubs += [v]*d
    rng.shuffle(stubs)
    adj = [set() for _ in range(n)]
    # naive pairing with restart on collision
    for _ in range(2000):
        rng.shuffle(stubs)
        ok = True
        adj = [set() for _ in range(n)]
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i+1]
            if a == b or b in adj[a]:
                ok = False
                break
            adj[a].add(b); adj[b].add(a)
        if ok:
            return adj
    raise RuntimeError("failed to generate simple d-regular graph")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--d", type=int, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    adj = random_regular_graph(args.n, args.d, args.seed)
    with open(args.out, "w") as f:
        json.dump({"n": args.n, "d": args.d, "seed": args.seed, "adj": [sorted(list(s)) for s in adj]}, f, indent=2)
    print(args.out)

if __name__ == "__main__":
    main()
