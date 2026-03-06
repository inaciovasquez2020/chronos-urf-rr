# toolkit/oblivion/scripts/cor_fok_coupling_test.py
# ADDITIONS: collision detector + collision histogram + top-colliding signatures

#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, collections, hashlib

def load_graph(path: str):
    with open(path, "r") as f:
        obj = json.load(f)
    n = obj.get("n")
    adj = obj.get("adj")
    if adj is None:
        edges = obj["edges"]
        if n is None:
            n = max(max(u,v) for u,v in edges) + 1
        adj = {str(i): [] for i in range(n)}
        for u,v in edges:
            adj[str(u)].append(v)
            adj[str(v)].append(u)
    return int(n), {int(k): list(map(int,v)) for k,v in adj.items()}

def ball_signature(adj, v: int, R: int):
    # deterministic BFS ball signature: multiset degrees at each layer + edge counts per layer pair
    from collections import deque, Counter
    dist = {v: 0}
    q = deque([v])
    layers = {0: [v]}
    while q:
        x = q.popleft()
        if dist[x] == R:
            continue
        for y in adj[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                layers.setdefault(dist[y], []).append(y)
                q.append(y)

    # layer degree multiset
    deg_layer = {r: dict(sorted(Counter(len(adj[u]) for u in layers.get(r, [])).items())) for r in range(R+1)}

    # inter-layer edge counts (r,r) and (r,r+1)
    layer_of = dist
    e_rr = {r: 0 for r in range(R+1)}
    e_rp = {r: 0 for r in range(R)}
    seen_edges = set()
    for x, nbrs in adj.items():
        if x not in layer_of:
            continue
        for y in nbrs:
            if y not in layer_of:
                continue
            a, b = (x,y) if x < y else (y,x)
            if (a,b) in seen_edges:
                continue
            seen_edges.add((a,b))
            rx, ry = layer_of[x], layer_of[y]
            if rx == ry:
                e_rr[rx] += 1
            elif abs(rx - ry) == 1:
                rmin = min(rx, ry)
                e_rp[rmin] += 1

    sig_obj = {"deg_layer": deg_layer, "e_rr": e_rr, "e_rp": e_rp}
    s = json.dumps(sig_obj, sort_keys=True, separators=(",",":")).encode("utf-8")
    h = hashlib.sha256(s).hexdigest()
    return h

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph_json", required=True)
    ap.add_argument("--R", type=int, required=True)
    ap.add_argument("--limit", type=int, default=6000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    n, adj = load_graph(args.graph_json)
    limit = min(args.limit, n)

    sigs = []
    for v in range(limit):
        sigs.append(ball_signature(adj, v, args.R))

    ctr = collections.Counter(sigs)
    distinct = len(ctr)
    max_mult = max(ctr.values()) if ctr else 0
    collisions = limit - distinct
    hist = dict(sorted(collections.Counter(ctr.values()).items()))

    # top-colliding signatures (up to 10)
    top = ctr.most_common(10)
    top = [{"sig": s, "mult": m} for (s,m) in top if m >= 2]

    out = {
        "meta": {
            "graph_json": args.graph_json,
            "n": n,
            "R": args.R,
            "limit": limit
        },
        "fok_proxy": {
            "distinct": distinct,
            "max_multiplicity": max_mult,
            "collisions": collisions,
            "multiplicity_histogram": hist,
            "top_collisions": top
        }
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
