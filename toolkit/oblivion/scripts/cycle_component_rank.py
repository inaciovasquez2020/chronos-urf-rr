#!/usr/bin/env python3

import argparse
import json
from collections import defaultdict


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


def find_cycles(adj, nodes, limit=8):
    cycles = []
    nodes = set(nodes)

    for u in nodes:
        stack = [(u, [u])]

        while stack:
            v, path = stack.pop()

            if len(path) > limit:
                continue

            for w in adj[v]:
                if w == u and len(path) >= 3:
                    cyc = tuple(sorted(path))
                    cycles.append(cyc)

                elif w not in path and w in nodes:
                    stack.append((w, path + [w]))

    return list(set(cycles))


def rank_f2(cycles):
    vecs = []
    index = {}
    c = 0

    for cyc in cycles:
        for e in cyc:
            if e not in index:
                index[e] = c
                c += 1

    for cyc in cycles:
        v = 0
        for e in cyc:
            v ^= (1 << index[e])
        vecs.append(v)

    r = 0

    while vecs:
        v = vecs.pop()

        if v == 0:
            continue

        r += 1
        p = v & -v

        new = []
        for x in vecs:
            if x & p:
                new.append(x ^ v)
            else:
                new.append(x)

        vecs = new

    return r


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--graph_json", required=True)
    parser.add_argument("--R", type=int, default=6)

    args = parser.parse_args()

    adj = load_graph(args.graph_json)

    cycles = []

    for v in range(min(len(adj), 500)):
        ball = bfs_ball(adj, v, args.R)
        cycles.extend(find_cycles(adj, ball))

    cycles = list(set(cycles))

    overlap_graph = defaultdict(set)

    for i in range(len(cycles)):
        for j in range(i + 1, len(cycles)):
            if set(cycles[i]) & set(cycles[j]):
                overlap_graph[i].add(j)
                overlap_graph[j].add(i)

    visited = set()
    components = []

    for i in range(len(cycles)):

        if i in visited:
            continue

        stack = [i]
        comp = []

        while stack:

            x = stack.pop()

            if x in visited:
                continue

            visited.add(x)
            comp.append(x)

            for y in overlap_graph[x]:
                stack.append(y)

        components.append(comp)

    comp_ranks = []

    for comp in components:
        comp_cycles = [cycles[i] for i in comp]
        r = rank_f2(comp_cycles)
        comp_ranks.append(r)

    result = {
        "cycle_count": len(cycles),
        "component_count": len(components),
        "largest_component": max(len(c) for c in components) if components else 0,
        "component_ranks": comp_ranks,
        "max_component_rank": max(comp_ranks) if comp_ranks else 0,
        "total_rank_sum": sum(comp_ranks)
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
