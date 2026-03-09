#!/usr/bin/env python3

import json
import hashlib
import networkx as nx

from toolkit.oblivion.cor.cycle_overlap_rank import cycle_incidence_rank


def rooted_radius_signature(G, root, R):
    layers = {root: 0}
    q = [root]
    order = [root]
    while q:
        v = q.pop(0)
        if layers[v] == R:
            continue
        for u in sorted(G.neighbors(v)):
            if u not in layers:
                layers[u] = layers[v] + 1
                q.append(u)
                order.append(u)
    verts = sorted(layers.keys(), key=lambda x: (layers[x], x))
    edges = []
    for i, u in enumerate(verts):
        for v in verts[i+1:]:
            if G.has_edge(u, v):
                edges.append((layers[u], layers[v]))
    payload = {
        "root_deg": G.degree(root),
        "layer_hist": [sum(1 for v in verts if layers[v] == r) for r in range(R+1)],
        "edge_profile": sorted(edges)
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def fo3_proxy_stats(G, R=3):
    sigs = {}
    for v in G.nodes():
        s = rooted_radius_signature(G, v, R)
        sigs[s] = sigs.get(s, 0) + 1
    return {
        "distinct_signatures": len(sigs),
        "max_multiplicity": max(sigs.values()),
        "histogram_top10": dict(sorted(sigs.items(), key=lambda kv: kv[1], reverse=True)[:10])
    }


def run():
    out = []
    for n in [200, 400, 800]:
        G = nx.random_regular_graph(4, n, seed=n)
        cor = cycle_incidence_rank(G)
        prox = fo3_proxy_stats(G, R=3)
        out.append({
            "family": "random_regular_4",
            "n": n,
            "cor_rank": cor["rank"],
            "cor_rank_over_n": cor["rank"] / n,
            "fo3_proxy_distinct": prox["distinct_signatures"],
            "fo3_proxy_max_mult": prox["max_multiplicity"]
        })
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
