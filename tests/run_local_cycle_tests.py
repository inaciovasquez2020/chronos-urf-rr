#!/usr/bin/env python3

import argparse
import json
import itertools
from collections import Counter


def load_graph(path):
    with open(path) as f:
        data = json.load(f)

    if "edges" in data:
        edges = data["edges"]

    elif "adj" in data:
        if isinstance(data["adj"], dict):
            edges = []
            for u, nb in data["adj"].items():
                u = int(u)
                for v in nb:
                    if u < v:
                        edges.append((u, v))

        elif isinstance(data["adj"], list):
            edges = []
            for u, nb in enumerate(data["adj"]):
                for v in nb:
                    if u < v:
                        edges.append((u, v))

        else:
            raise RuntimeError("adj format not recognized")

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


def count_local_cycles(adj, ball, limit=8):
    cycles = set()
    nodes = list(ball)

    for u in nodes:
        stack = [(u, [u])]

        while stack:
            v, path = stack.pop()

            if len(path) > limit:
                continue

            for w in adj[v]:

                if w == u and len(path) >= 3:
                    cyc = tuple(sorted(path))
                    cycles.add(cyc)

                elif w not in path and w in ball:
                    stack.append((w, path + [w]))

    return cycles


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


def wl_colors(adj, steps=5):
    n = len(adj)

    col = [len(adj[v]) for v in range(n)]

    for _ in range(steps):

        new = []

        for v in range(n):

            sig = (
                col[v],
                tuple(sorted(col[u] for u in adj[v]))
            )

            new.append(hash(sig))

        col = new

    return col


def main():

    ap = argparse.ArgumentParser()

    ap.add_argument("--graph_json", required=True)
    ap.add_argument("--R", type=int, default=3)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--delta", type=int, default=4)

    ap.add_argument(
        "--tests",
        nargs="+",
        default=[]
    )

    args = ap.parse_args()

    adj = load_graph(args.graph_json)
    n = len(adj)

    out = {}

    if "local_generators" in args.tests:

        all_cycles = set()

        for v in range(n):

            ball = bfs_ball(adj, v, args.R)

            cyc = count_local_cycles(adj, ball)

            all_cycles |= cyc

        out["local_cycle_count"] = len(all_cycles)
        out["COR_R"] = rank_f2(all_cycles)

    if "ef_detectability" in args.tests:

        sizes = []

        for v in range(min(n, 200)):

            ball = bfs_ball(adj, v, args.R)

            sizes.append(len(ball))

        out["ball_sizes"] = Counter(sizes)

    if "overlap" in args.tests:

        overlaps = 0

        for v in range(min(n, 200)):

            ball = bfs_ball(adj, v, args.R)

            cyc = list(count_local_cycles(adj, ball))

            for a, b in itertools.combinations(cyc, 2):

                if set(a) & set(b):
                    overlaps += 1

        out["cycle_overlaps"] = overlaps

    if "parity" in args.tests:

        parity = []

        for v in range(min(n, 200)):

            ball = bfs_ball(adj, v, args.R)

            cyc = count_local_cycles(adj, ball)

            for c in cyc:
                parity.append(len(c) % 2)

        out["cycle_parity_hist"] = Counter(parity)

    if "wlk" in args.tests:

        col = wl_colors(adj, 5)

        out["distinct_wl_colors"] = len(set(col))

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
