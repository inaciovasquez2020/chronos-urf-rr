#!/usr/bin/env python3
import argparse, json

def torus(n):
    N = n*n
    adj = [set() for _ in range(N)]
    def vid(i,j): return (i % n)*n + (j % n)
    for i in range(n):
        for j in range(n):
            v = vid(i,j)
            for (a,b) in [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]:
                w = vid(a,b)
                adj[v].add(w)
    return adj

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    adj = torus(args.n)
    with open(args.out,"w") as f:
        json.dump({"meta":{"graph":"torus","n_side":args.n,"N":len(adj)},"adj":[sorted(list(s)) for s in adj]}, f)
    print(args.out)

if __name__ == "__main__":
    main()
