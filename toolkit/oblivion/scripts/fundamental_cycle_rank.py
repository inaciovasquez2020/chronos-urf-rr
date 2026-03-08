#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict, deque

import networkx as nx
import numpy as np


def random_lift_k4(p: int, seed: int) -> nx.Graph:
    rng = np.random.default_rng(seed)
    base_vertices = [0, 1, 2, 3]
    base_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    perms = {}
    for e in base_edges:
        perms[e] = rng.permutation(p)

    G = nx.Graph()
    for u in base_vertices:
        for i in range(p):
            G.add_node((u, int(i)))

    for (u, v) in base_edges:
        pi = perms[(u, v)]
        for i in range(p):
            G.add_edge((u, int(i)), (v, int(pi[i])))

    return G


def random_regular_graph(n: int, d: int, seed: int) -> nx.Graph:
    return nx.random_regular_graph(d, n, seed=seed)


def bfs_tree_with_parent(G: nx.Graph, root) -> tuple[set[tuple[int, int]], dict, dict]:
    parent = {root: None}
    depth = {root: 0}
    q = deque([root])
    tree_edges = set()

    while q:
        u = q.popleft()
        for v in G.neighbors(u):
            if v not in parent:
                parent[v] = u
                depth[v] = depth[u] + 1
                tree_edges.add(tuple(sorted((u, v))))
                q.append(v)

    return tree_edges, parent, depth


def path_to_root(parent: dict, u):
    path = []
    while u is not None:
        path.append(u)
        u = parent[u]
    return path


def tree_path_edges(parent: dict, u, v) -> list[tuple]:
    pu = path_to_root(parent, u)
    pv = path_to_root(parent, v)
    pos = {x: i for i, x in enumerate(pu)}
    lca = None
    jv = None
    for j, x in enumerate(pv):
        if x in pos:
            lca = x
            jv = j
            break

    iu = pos[lca]
    path_nodes = pu[:iu + 1] + list(reversed(pv[:jv]))
    edges = []
    for i in range(len(path_nodes) - 1):
        edges.append(tuple(sorted((path_nodes[i], path_nodes[i + 1]))))
    return edges


def fundamental_cycles(G: nx.Graph, root, max_cycle_len: int | None = None) -> list[list[tuple]]:
    tree_edges, parent, depth = bfs_tree_with_parent(G, root)
    all_edges = {tuple(sorted(e)) for e in G.edges()}
    non_tree_edges = sorted(all_edges - tree_edges)
    cycles = []

    for e in non_tree_edges:
        u, v = e
        if u not in parent or v not in parent:
            continue
        path_edges = tree_path_edges(parent, u, v)
        cyc = path_edges + [e]
        cyc = list(dict.fromkeys(cyc))
        if max_cycle_len is None or len(cyc) <= max_cycle_len:
            cycles.append(cyc)

    return cycles


def node_balls(G: nx.Graph, R: int) -> dict:
    balls = {}
    for v in G.nodes():
        seen = {v}
        q = deque([(v, 0)])
        while q:
            u, dist = q.popleft()
            if dist == R:
                continue
            for w in G.neighbors(u):
                if w not in seen:
                    seen.add(w)
                    q.append((w, dist + 1))
        balls[v] = seen
    return balls


def cycle_in_some_radius_ball(cycle_edges: list[tuple], balls: dict) -> bool:
    cycle_vertices = set()
    for u, v in cycle_edges:
        cycle_vertices.add(u)
        cycle_vertices.add(v)
    for B in balls.values():
        if cycle_vertices.issubset(B):
            return True
    return False


def incidence_matrix(G: nx.Graph, cycles: list[list[tuple]]) -> np.ndarray:
    edges = [tuple(sorted(e)) for e in G.edges()]
    idx = {e: i for i, e in enumerate(edges)}
    M = np.zeros((len(cycles), len(edges)), dtype=np.uint8)
    for r, cyc in enumerate(cycles):
        for e in cyc:
            if e in idx:
                M[r, idx[e]] = 1
    return M


def rank_f2(M: np.ndarray) -> int:
    M = (M.copy() % 2).astype(np.uint8)
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if M[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            M[[r, pivot]] = M[[pivot, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
        if r == rows:
            break
    return int(r)


def analyze_graph(G: nx.Graph, R: int, root=None, max_cycle_len: int | None = None) -> dict:
    if root is None:
        root = next(iter(G.nodes()))
    cycles = fundamental_cycles(G, root=root, max_cycle_len=max_cycle_len)
    balls = node_balls(G, R)
    local_cycles = [cyc for cyc in cycles if cycle_in_some_radius_ball(cyc, balls)]

    M_global = incidence_matrix(G, cycles)
    M_local = incidence_matrix(G, local_cycles)

    n = G.number_of_nodes()
    m = G.number_of_edges()
    cycle_rank_exact = m - n + nx.number_connected_components(G)

    out = {
        "n": n,
        "m": m,
        "R": R,
        "root": str(root),
        "fundamental_cycles": len(cycles),
        "local_fundamental_cycles": len(local_cycles),
        "rank_F2_global_sample": rank_f2(M_global),
        "rank_F2_local_sample": rank_f2(M_local),
        "cycle_space_dimension_exact": cycle_rank_exact,
        "local_rank_over_n": float(rank_f2(M_local) / n) if n else 0.0,
        "global_rank_over_n": float(rank_f2(M_global) / n) if n else 0.0,
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="family", required=True)

    ap_rr = sub.add_parser("rr")
    ap_rr.add_argument("--n", type=int, required=True)
    ap_rr.add_argument("--d", type=int, default=4)
    ap_rr.add_argument("--seed", type=int, default=0)
    ap_rr.add_argument("--R", type=int, default=8)
    ap_rr.add_argument("--max-cycle-len", type=int, default=None)
    ap_rr.add_argument("--out", required=True)

    ap_lift = sub.add_parser("liftk4")
    ap_lift.add_argument("--p", type=int, required=True)
    ap_lift.add_argument("--seed", type=int, default=0)
    ap_lift.add_argument("--R", type=int, default=8)
    ap_lift.add_argument("--max-cycle-len", type=int, default=None)
    ap_lift.add_argument("--out", required=True)

    args = ap.parse_args()

    if args.family == "rr":
        G = random_regular_graph(args.n, args.d, args.seed)
        out = analyze_graph(G, R=args.R, max_cycle_len=args.max_cycle_len)
        out["family"] = "random_regular"
        out["d"] = args.d
        out["seed"] = args.seed
    else:
        G = random_lift_k4(args.p, args.seed)
        out = analyze_graph(G, R=args.R, max_cycle_len=args.max_cycle_len)
        out["family"] = "random_lift_K4"
        out["p"] = args.p
        out["seed"] = args.seed

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
