#!/usr/bin/env python3
import argparse, json, random
from collections import deque, Counter

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
    sub = [sorted(idx[w] for w in adj[v] if w in idx) for v in nodes]
    return sub

def wl_color_refinement(sub_adj, rounds):
    # 1-WL on rooted ball: stable color refinement (cheap FO^k proxy)
    n = len(sub_adj)
    col = [1]*n
    for _ in range(rounds):
        sigs = []
        for v in range(n):
            sig = (col[v], tuple(sorted(col[w] for w in sub_adj[v])))
            sigs.append(sig)
        # compress
        mp = {}
        nxt = []
        for s in sigs:
            if s not in mp:
                mp[s] = len(mp)+1
            nxt.append(mp[s])
        col = nxt
    return tuple(col)

def load_graph(path):
    with open(path,"r") as f:
        obj = json.load(f)
    if "adj" in obj:
        adj = [set(nei) for nei in obj["adj"]]
        return adj
    raise ValueError("expected json with key 'adj' as adjacency lists")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph_json", required=True)
    ap.add_argument("--R", type=int, default=2)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--out", default="toolkit/oblivion/results/fo_proxy_type_collisions.json")
    args = ap.parse_args()

    adj = load_graph(args.graph_json)
    n = len(adj)

    sigs = []
    for v in range(n):
        ball = induced_ball(adj, v, args.R)
        sigs.append(wl_color_refinement(ball, args.rounds))

    ctr = Counter(sigs)
    payload = {
        "meta": {"graph_json": args.graph_json, "n": n, "R": args.R, "rounds": args.rounds},
        "type_count": len(ctr),
        "max_multiplicity": max(ctr.values()) if ctr else 0,
        "histogram": dict(sorted(Counter(ctr.values()).items()))
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
