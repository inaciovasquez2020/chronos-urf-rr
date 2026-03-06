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

def induced_subgraph(adj, nodes):
    idx = {v:i for i,v in enumerate(nodes)}
    sub = [set() for _ in nodes]
    for v in nodes:
        for w in adj[v]:
            if w in idx:
                sub[idx[v]].add(idx[w])
    return sub

def cycle_rank_mod2(sub_adj):
    n = len(sub_adj)
    m2 = sum(len(sub_adj[v]) for v in range(n))
    m = m2 // 2
    seen = [False]*n
    c = 0
    for s in range(n):
        if not seen[s]:
            c += 1
            dq = deque([s]); seen[s]=True
            while dq:
                u=dq.popleft()
                for w in sub_adj[u]:
                    if not seen[w]:
                        seen[w]=True
                        dq.append(w)
    return m - n + c

def xor_basis_insert(basis, x):
    while x:
        hb = x.bit_length() - 1
        if hb not in basis:
            basis[hb] = x
            return 1
        x ^= basis[hb]
    return 0

def fundamental_cycles_bitvectors(adj, nodes, eidx):
    S = set(nodes)
    parent = {}
    pedge = {}
    depth = {}
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

    V = range(n) if args.limit_vertices <= 0 else range(min(n, args.limit_vertices))

    sum_local = 0
    basis = {}
    insertions = 0
    total_cycle_vecs = 0

    for v in V:
        nodes = ball_nodes(adj, v, args.R)
        sub = induced_subgraph(adj, nodes)
        sum_local += cycle_rank_mod2(sub)

        vecs = fundamental_cycles_bitvectors(adj, nodes, eidx)
        total_cycle_vecs += len(vecs)
        for x in vecs:
            insertions += xor_basis_insert(basis, x)

    global_span = len(basis)
    dep_overlap = sum_local - global_span

    payload = {
        "meta": {"graph_json": args.graph_json, "R": args.R, "n": n, "m": m, "limit_vertices": args.limit_vertices},
        "sum_local_cycle_rank": sum_local,
        "global_ball_cycle_span_rank": global_span,
        "dependency_overlap": dep_overlap,
        "cycle_vectors_total": total_cycle_vecs,
        "basis_insertions": insertions,
        "source_meta": meta
    }

    with open(args.out,"w") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
