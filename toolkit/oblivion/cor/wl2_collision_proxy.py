#!/usr/bin/env python3

import json
import hashlib
import networkx as nx

from toolkit.oblivion.cor.cycle_overlap_rank import cycle_incidence_rank


def initial_colors(G):
    return {v: str(G.degree(v)) for v in G.nodes()}


def wl2_round(G, colors):
    new_colors = {}
    for v in G.nodes():
        multiset = sorted(colors[u] for u in G.neighbors(v))
        raw = colors[v] + "|" + "|".join(multiset)
        new_colors[v] = hashlib.sha256(raw.encode()).hexdigest()
    return new_colors


def wl_stabilize(G, rounds=6):
    colors = initial_colors(G)
    for _ in range(rounds):
        colors = wl2_round(G, colors)
    return colors


def collision_stats(G, rounds=6):
    colors = wl_stabilize(G, rounds=rounds)
    freq = {}
    for c in colors.values():
        freq[c] = freq.get(c, 0) + 1
    return {
        "distinct_colors": len(freq),
        "max_multiplicity": max(freq.values()),
        "collision_histogram": dict(sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:10])
    }


def run():
    out = []
    for n in [200, 400, 800]:
        G = nx.random_regular_graph(4, n, seed=n)
        cor = cycle_incidence_rank(G)
        wl = collision_stats(G, rounds=6)
        out.append({
            "n": n,
            "cor_rank": cor["rank"],
            "cor_rank_over_n": cor["rank"] / n,
            "distinct_wl_colors": wl["distinct_colors"],
            "max_wl_multiplicity": wl["max_multiplicity"]
        })
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
