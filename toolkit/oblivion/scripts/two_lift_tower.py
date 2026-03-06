#!/usr/bin/env python3
import argparse, json, random

def load_adj(path):
    with open(path,"r") as f:
        obj = json.load(f)
    return [list(nei) for nei in obj["adj"]], obj.get("meta", {})

def two_lift(adj, rng):
    n = len(adj)
    N = 2*n
    out = [set() for _ in range(N)]
    done = set()
    for u in range(n):
        for v in adj[u]:
            if u < v and (u,v) not in done:
                done.add((u,v))
                s = rng.getrandbits(1)  # 0 parallel, 1 crossed
                for a in [0,1]:
                    uu = u + a*n
                    vv = v + ((a ^ s)*n)
                    out[uu].add(vv); out[vv].add(uu)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--levels", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out_prefix", required=True)
    args = ap.parse_args()

    base, meta = load_adj(args.inp)
    rng = random.Random(args.seed)

    cur = [set(nei) for nei in base]
    for t in range(1, args.levels+1):
        cur = two_lift(cur, rng)
        path = f"{args.out_prefix}_L{t}.json"
        payload = {"meta":{"two_lift_level":t,"seed":args.seed,"source":args.inp,"N":len(cur), "base_meta":meta},
                   "adj":[sorted(list(s)) for s in cur]}
        with open(path,"w") as f:
            json.dump(payload, f)
        print(path)

if __name__ == "__main__":
    main()
