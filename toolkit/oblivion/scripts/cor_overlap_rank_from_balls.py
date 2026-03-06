#!/usr/bin/env python3
import argparse, json
from collections import deque

def load_adj(path):
    with open(path,"r") as f:
        obj = json.load(f)
    return [set(nei) for nei in obj["adj"]], obj.get("meta", {})

def build_edge_index(adj):
    n = len(adj)
    edges = {}
    idx = 0
    for u in range(n):
        for v in adj[u]:
            if u < v:
                edges[(u,v)] = idx
                idx += 1
    return edges, idx

def ball_nodes(adj, root, R):
    dist = {root: 0}
    q = deque([root])
    while q:
        u = q.popleft()
        if dist[u] == R:
            continue
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    return list(dist.keys())

def xor_basis_insert(basis, x):
    while x:
        hb = x.bit_length() - 1
        if hb not in basis:
            basis[hb] = x
            return True
        x ^= basis[hb]
    return False

def cycle_vectors(adj, nodes, eidx):
    S = set(nodes)
    parent = {}
    pedge = {}
    depth = {}
    from collections import deque
    for s in nodes:
        if s in depth:
            continue
        depth[s] = 0
        parent[s] = -1
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in S:
                    continue
                if v not in depth:
                    depth[v] = depth[u] + 1
                    parent[v] = u
                    a,b = (u,v) if u < v else (v,u)
                    pedge[v] = eidx[(a,b)]
                    q.append(v)
    in_tree = set(pedge.values())
    vecs = []
    for u in nodes:
        for v in adj[u]:
            if v not in S or u >= v:
                continue
            eid = eidx[(u,v)]
            if eid in in_tree:
                continue
            x = 0
            x ^= (1 << eid)
            uu, vv = u, v
            while uu != vv:
                if depth[uu] >= depth[vv]:
                    if parent[uu] == -1: break
                    x ^= (1 << pedge[uu])
                    uu = parent[uu]
                else:
                    if parent[vv] == -1: break
                    x ^= (1 << pedge[vv])
                    vv = parent[vv]
            vecs.append(x)
    return vecs

def overlap(a,b):
    return (a & b) != 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph_json", required=True)
    ap.add_argument("--R", type=int, default=2)
    ap.add_argument("--limit_vertices", type=int, default=0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    adj, meta = load_adj(args.graph_json)
    eidx, m = build_edge_index(adj)
    n = len(adj)

    cycles = []
    V = range(n) if args.limit_vertices <= 0 else range(min(n, args.limit_vertices))
    for v in V:
        nodes = ball_nodes(adj, v, args.R)
        cycles.extend(cycle_vectors(adj, nodes, eidx))

    basis = {}
    kept = []
    for c in cycles:
        if any(overlap(c,k) for k in kept):
            if xor_basis_insert(basis, c):
                kept.append(c)

    payload = {
        "meta": {"graph_json": args.graph_json, "R": args.R, "n": n, "m": m},
        "overlap_rank": len(basis),
        "cycles_examined": len(cycles),
        "kept_cycles": len(kept),
        "source_meta": meta
    }

    with open(args.out,"w") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
