#!/usr/bin/env python3
import argparse
import hashlib
import json
from collections import deque

import networkx as nx
import numpy as np


def random_regular_graph(n: int, d: int, seed: int) -> nx.Graph:
    return nx.random_regular_graph(d, n, seed=seed)


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


def bfs_tree_with_parent(G: nx.Graph, root):
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


def path_to_root(parent, u):
    path = []
    while u is not None:
        path.append(u)
        u = parent[u]
    return path


def tree_path_edges(parent, u, v):
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
    path_nodes = pu[: iu + 1] + list(reversed(pv[:jv]))
    edges = []
    for i in range(len(path_nodes) - 1):
        edges.append(tuple(sorted((path_nodes[i], path_nodes[i + 1]))))
    return edges


def fundamental_cycles(G: nx.Graph, root):
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
        cycles.append(cyc)

    return cycles


def ball_nodes(G: nx.Graph, root, R: int):
    seen = {root}
    q = deque([(root, 0)])
    while q:
        u, dist = q.popleft()
        if dist == R:
            continue
        for w in G.neighbors(u):
            if w not in seen:
                seen.add(w)
                q.append((w, dist + 1))
    return seen


def rooted_ball_signature(G: nx.Graph, root, R: int) -> str:
    B = ball_nodes(G, root, R)
    H = G.subgraph(B).copy()
    dist = nx.single_source_shortest_path_length(H, root, cutoff=R)
    data = []
    for u in sorted(H.nodes(), key=lambda x: str(x)):
        nbr_dists = sorted(dist.get(v, R + 1) for v in H.neighbors(u))
        data.append((dist.get(u, R + 1), H.degree(u), tuple(nbr_dists)))
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()


def vertex_orbits_by_ball_type(G: nx.Graph, R: int):
    sig = {}
    orbit_index = {}
    next_id = 0
    for v in G.nodes():
        h = rooted_ball_signature(G, v, R)
        sig[v] = h
        if h not in orbit_index:
            orbit_index[h] = next_id
            next_id += 1
    return {v: orbit_index[sig[v]] for v in G.nodes()}, orbit_index


def edge_orbits(G: nx.Graph, vertex_orbit_map):
    e_orbits = {}
    orbit_index = {}
    next_id = 0
    for u, v in G.edges():
        key = tuple(sorted((vertex_orbit_map[u], vertex_orbit_map[v])))
        if key not in orbit_index:
            orbit_index[key] = next_id
            next_id += 1
        e_orbits[tuple(sorted((u, v)))] = orbit_index[key]
    return e_orbits, orbit_index


def cycle_orbit_signature(cycle_edges, e_orbits):
    sig = sorted(e_orbits[tuple(sorted(e))] for e in cycle_edges)
    return tuple(sig)


def compressed_cycle_orbit_matrix(G: nx.Graph, cycles, R: int):
    v_orbits, v_orbit_index = vertex_orbits_by_ball_type(G, R)
    e_orbits, e_orbit_index = edge_orbits(G, v_orbits)

    row_orbit_index = {}
    rows = []
    next_row = 0

    for cyc in cycles:
        rsig = cycle_orbit_signature(cyc, e_orbits)
        if rsig not in row_orbit_index:
            row_orbit_index[rsig] = next_row
            next_row += 1
            row = np.zeros(len(e_orbit_index), dtype=np.uint8)
            for e in cyc:
                row[e_orbits[tuple(sorted(e))]] ^= 1
            rows.append(row)

    if rows:
        M = np.vstack(rows)
    else:
        M = np.zeros((0, len(e_orbit_index)), dtype=np.uint8)

    return M, v_orbit_index, e_orbit_index, row_orbit_index


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


def incidence_matrix(G: nx.Graph, cycles):
    edges = [tuple(sorted(e)) for e in G.edges()]
    idx = {e: i for i, e in enumerate(edges)}
    M = np.zeros((len(cycles), len(edges)), dtype=np.uint8)
    for r, cyc in enumerate(cycles):
        for e in cyc:
            M[r, idx[tuple(sorted(e))]] ^= 1
    return M


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="family", required=True)

    ap_rr = sub.add_parser("rr")
    ap_rr.add_argument("--n", type=int, required=True)
    ap_rr.add_argument("--d", type=int, default=4)
    ap_rr.add_argument("--seed", type=int, default=0)
    ap_rr.add_argument("--R", type=int, default=4)
    ap_rr.add_argument("--out", required=True)

    ap_lift = sub.add_parser("liftk4")
    ap_lift.add_argument("--p", type=int, required=True)
    ap_lift.add_argument("--seed", type=int, default=0)
    ap_lift.add_argument("--R", type=int, default=4)
    ap_lift.add_argument("--out", required=True)

    args = ap.parse_args()

    if args.family == "rr":
        G = random_regular_graph(args.n, args.d, args.seed)
        meta = {"family": "random_regular", "n": args.n, "d": args.d, "seed": args.seed, "R": args.R}
    else:
        G = random_lift_k4(args.p, args.seed)
        meta = {"family": "random_lift_K4", "p": args.p, "seed": args.seed, "R": args.R}

    root = next(iter(G.nodes()))
    cycles = fundamental_cycles(G, root)
    M_full = incidence_matrix(G, cycles)
    M_comp, v_orbit_index, e_orbit_index, row_orbit_index = compressed_cycle_orbit_matrix(G, cycles, args.R)

    out = {
        **meta,
        "graph_n": G.number_of_nodes(),
        "graph_m": G.number_of_edges(),
        "fundamental_cycles": len(cycles),
        "cycle_space_dimension_exact": G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G),
        "full_rank_F2": rank_f2(M_full),
        "vertex_ball_orbit_count": len(v_orbit_index),
        "edge_orbit_count": len(e_orbit_index),
        "cycle_orbit_count": len(row_orbit_index),
        "compressed_rank_F2": rank_f2(M_comp),
        "compressed_shape": list(M_comp.shape),
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
