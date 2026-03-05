#!/usr/bin/env python3
import argparse
import json
from collections import deque, defaultdict

def load_graph(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict) and "edges" in data:
        edges = data["edges"]
    else:
        edges = data
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj

def ball(adj, start, R):
    q = deque([(start, 0)])
    seen = {start}
    nodes = {start}
    while q:
        v, d = q.popleft()
        if d == R:
            continue
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                nodes.add(w)
                q.append((w, d + 1))
    return nodes

def beta1(adj, nodes):
    e = 0
    for v in nodes:
        for w in adj[v]:
            if w in nodes:
                e += 1
    e //= 2
    v = len(nodes)
    c = 1
    return e - v + c

def compute_signature(adj, v0, Rmax):
    out = []
    for R in range(1, Rmax + 1):
        B = ball(adj, v0, R)
        size = len(B)
        b1 = beta1(adj, B)
        rho = b1 / size if size > 0 else 0
        out.append({
            "R": R,
            "|B_R|": size,
            "beta1": b1,
            "rho": rho
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph_json", required=True)
    ap.add_argument("--root", type=int, default=0)
    ap.add_argument("--Rmax", type=int, default=10)
    args = ap.parse_args()

    adj = load_graph(args.graph_json)
    sig = compute_signature(adj, args.root, args.Rmax)

    print(json.dumps(sig, indent=2))

if __name__ == "__main__":
    main()
