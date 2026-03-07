#!/usr/bin/env python3

import argparse
import json
import random
from collections import defaultdict


def load_graph(path):
    with open(path) as f:
        data = json.load(f)

    edges = []

    if "edges" in data:
        edges = data["edges"]

    elif "adj" in data:

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


def bfs_ball(adj, start, R):

    seen = {start}
    frontier = [start]

    for _ in range(R):

        nxt = []

        for v in frontier:
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    nxt.append(w)

        frontier = nxt

    return seen


def sample_ball(adj, R):

    start = random.randrange(len(adj))
    ball = bfs_ball(adj, start, R)

    nodes = list(ball)
    idmap = {v: i for i, v in enumerate(nodes)}

    new_adj = [set() for _ in nodes]

    for v in nodes:
        for w in adj[v]:
            if w in idmap:
                new_adj[idmap[v]].add(idmap[w])

    return new_adj


def find_cycles(adj, nodes, max_len=8):

    cycles = set()
    nodes = set(nodes)

    for start in nodes:

        stack = [(start, [start])]

        while stack:

            v, path = stack.pop()

            if len(path) > max_len:
                continue

            for w in adj[v]:

                if w == start and len(path) >= 3:

                    cyc = tuple(sorted(path))
                    cycles.add(cyc)

                elif w not in path and w in nodes:

                    stack.append((w, path + [w]))

    return list(cycles)


def edge_cycle_counts(cycles):

    counts = defaultdict(int)

    for cyc in cycles:

        for i in range(len(cyc)):

            u = cyc[i]
            v = cyc[(i + 1) % len(cyc)]

            if u > v:
                u, v = v, u

            counts[(u, v)] += 1

    return counts


def vertex_transport_signature(v, adj, edge_counts):

    vec = []

    for u in adj[v]:

        a, b = min(u, v), max(u, v)
        vec.append(edge_counts.get((a, b), 0))

    vec.sort()

    return (len(adj[v]), tuple(vec))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--graph_json", required=True)
    parser.add_argument("--R", type=int, default=6)
    parser.add_argument("--samples", default="50,100,200,400,600,800")

    args = parser.parse_args()

    adj = load_graph(args.graph_json)

    sizes = [int(x) for x in args.samples.split(",")]

    for s in sizes:

        sub = sample_ball(adj, args.R)

        nodes = list(range(len(sub)))

        all_cycles = []

        for v in nodes:

            ball = bfs_ball(sub, v, args.R)
            all_cycles.extend(find_cycles(sub, ball))

        cycles = list(set(all_cycles))

        edge_counts = edge_cycle_counts(cycles)

        sigs = set()

        for v in nodes:

            sig = vertex_transport_signature(v, sub, edge_counts)
            sigs.add(sig)

        print(json.dumps({
            "sample_index": s,
            "nodes": len(sub),
            "cycles": len(cycles),
            "distinct_transport_signatures": len(sigs)
        }))


if __name__ == "__main__":
    main()
