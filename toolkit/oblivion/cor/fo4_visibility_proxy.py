#!/usr/bin/env python3

import json
import hashlib
import itertools
import networkx as nx

from toolkit.oblivion.cor.cycle_overlap_rank import cycle_incidence_rank


def bfs_ball(G, roots, R):
    dist = {}
    q = []
    for i, r in enumerate(roots):
        key = ("r", i, r)
        dist[r] = 0
        q.append(r)
    head = 0
    while head < len(q):
        v = q[head]
        head += 1
        if dist[v] == R:
            continue
        for u in sorted(G.neighbors(v)):
            if u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist


def pair_root_signature(G, a, b, R):
    ball = bfs_ball(G, (a, b), R)
    verts = sorted(ball.keys(), key=lambda x: (ball[x], x))
    da = nx.single_source_shortest_path_length(G, a, cutoff=R)
    db = nx.single_source_shortest_path_length(G, b, cutoff=R)

    layer_hist = {}
    for v in verts:
        xa = da.get(v, R + 1)
        xb = db.get(v, R + 1)
        key = (min(xa, R + 1), min(xb, R + 1))
        layer_hist[key] = layer_hist.get(key, 0) + 1

    edge_profile = []
    for i, u in enumerate(verts):
        for v in verts[i + 1:]:
            if G.has_edge(u, v):
                edge_profile.append((
                    min(da.get(u, R + 1), R + 1),
                    min(db.get(u, R + 1), R + 1),
                    min(da.get(v, R + 1), R + 1),
                    min(db.get(v, R + 1), R + 1)
                ))

    common_neighbors = len(set(G.neighbors(a)).intersection(set(G.neighbors(b))))
    dist_ab = nx.shortest_path_length(G, a, b) if nx.has_path(G, a, b) else None

    payload = {
        "deg_a": G.degree(a),
        "deg_b": G.degree(b),
        "adjacent": 1 if G.has_edge(a, b) else 0,
        "dist_ab": dist_ab,
        "common_neighbors": common_neighbors,
        "layer_hist": sorted((list(k), v) for k, v in layer_hist.items()),
        "edge_profile": sorted(edge_profile),
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def fo4_proxy_stats(G, R=3, max_pairs=4000):
    verts = list(G.nodes())
    pairs = []
    for a, b in itertools.combinations(verts, 2):
        pairs.append((a, b))
        if len(pairs) >= max_pairs:
            break

    freq = {}
    for a, b in pairs:
        s = pair_root_signature(G, a, b, R)
        freq[s] = freq.get(s, 0) + 1

    return {
        "pairs_sampled": len(pairs),
        "distinct_pair_signatures": len(freq),
        "max_multiplicity": max(freq.values()) if freq else 0,
        "top10": dict(sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:10]),
    }


def run_random_regular():
    out = []
    for n in [200, 400, 800]:
        G = nx.random_regular_graph(4, n, seed=n)
        cor = cycle_incidence_rank(G)
        prox = fo4_proxy_stats(G, R=3, max_pairs=4000)
        out.append({
            "family": "random_regular_4",
            "n": n,
            "cor_rank": cor["rank"],
            "cor_rank_over_n": cor["rank"] / n,
            "fo4_pair_distinct": prox["distinct_pair_signatures"],
            "fo4_pair_max_mult": prox["max_multiplicity"],
            "pairs_sampled": prox["pairs_sampled"],
        })
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run_random_regular()
