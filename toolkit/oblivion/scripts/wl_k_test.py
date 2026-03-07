#!/usr/bin/env python3

import argparse
import json
import random
from collections import Counter


def load_graph(path):
    with open(path) as f:
        data = json.load(f)

    if "edges" in data:
        edges = data["edges"]

    elif "adj" in data:
        edges = []

        if isinstance(data["adj"], list):
            for u, nb in enumerate(data["adj"]):
                for v in nb:
                    if u < v:
                        edges.append((u, v))

        else:
            for u, nb in data["adj"].items():
                u = int(u)
                for v in nb:
                    if u < v:
                        edges.append((u, v))
    else:
        raise RuntimeError("graph format not recognized")

    n = max(max(u, v) for u, v in edges) + 1
    adj = [set() for _ in range(n)]

    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    return adj


def induced_subgraph(adj, nodes):
    nodes = list(nodes)
    idmap = {v: i for i, v in enumerate(nodes)}
    new_adj = [set() for _ in nodes]

    for v in nodes:
        for w in adj[v]:
            if w in idmap:
                new_adj[idmap[v]].add(idmap[w])

    return new_adj


def sample_subgraph(adj, size):
    n = len(adj)
    nodes = random.sample(range(n), size)
    return induced_subgraph(adj, nodes)


def wl1(adj, rounds=5):

    n = len(adj)
    colors = [len(adj[v]) for v in range(n)]

    for _ in range(rounds):

        palette = {}
        next_id = 0
        new_colors = []

        for v in range(n):

            sig = (
                colors[v],
                tuple(sorted(colors[u] for u in adj[v]))
            )

            if sig not in palette:
                palette[sig] = next_id
                next_id += 1

            new_colors.append(palette[sig])

        if new_colors == colors:
            break

        colors = new_colors

    return colors


def wl2(adj, rounds=4):

    n = len(adj)

    pairs = {}
    pair_list = []

    for u in range(n):
        for v in range(n):

            if u == v:
                c = 2
            elif v in adj[u]:
                c = 1
            else:
                c = 0

            pairs[(u, v)] = c
            pair_list.append((u, v))

    for _ in range(rounds):

        palette = {}
        next_id = 0
        new_pairs = {}

        for u, v in pair_list:

            ext = []

            for w in range(n):
                ext.append((pairs[(u, w)], pairs[(w, v)]))

            sig = (pairs[(u, v)], tuple(sorted(ext)))

            if sig not in palette:
                palette[sig] = next_id
                next_id += 1

            new_pairs[(u, v)] = palette[sig]

        if all(new_pairs[p] == pairs[p] for p in pair_list):
            break

        pairs = new_pairs

    vertex_colors = []

    for u in range(n):
        sig = tuple(sorted(pairs[(u, v)] for v in range(n)))
        vertex_colors.append(sig)

    palette = {}
    next_id = 0
    compressed = []

    for sig in vertex_colors:
        if sig not in palette:
            palette[sig] = next_id
            next_id += 1
        compressed.append(palette[sig])

    return compressed


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--graph_json", required=True)
    parser.add_argument("--k", type=int, required=True)

    parser.add_argument("--sample", type=int, default=250)

    args = parser.parse_args()

    adj = load_graph(args.graph_json)

    if args.sample < len(adj):
        adj = sample_subgraph(adj, args.sample)

    if args.k == 1:
        colors = wl1(adj)

    elif args.k == 2:
        colors = wl2(adj)

    else:
        raise RuntimeError("subgraph mode supports k=1 or k=2")

    hist = Counter(colors)

    print(json.dumps({
        "sample_vertices": len(adj),
        "k": args.k,
        "distinct_colors": len(hist),
        "color_histogram": hist
    }, indent=2))


if __name__ == "__main__":
    main()
