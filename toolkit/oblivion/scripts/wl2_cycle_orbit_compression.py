#!/usr/bin/env python3
import argparse
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
    perms = {e: rng.permutation(p) for e in base_edges}

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
    q = deque([root])
    tree_edges = set()
    while q:
        u = q.popleft()
        for v in G.neighbors(u):
            if v not in parent:
                parent[v] = u
                tree_edges.add(tuple(sorted((u, v))))
                q.append(v)
    return tree_edges, parent


def path_to_root(parent, u):
    out = []
    while u is not None:
        out.append(u)
        u = parent[u]
    return out


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
    nodes = pu[:iu + 1] + list(reversed(pv[:jv]))
    edges = []
    for i in range(len(nodes) - 1):
        edges.append(tuple(sorted((nodes[i], nodes[i + 1]))))
    return edges


def fundamental_cycles(G: nx.Graph, root):
    tree_edges, parent = bfs_tree_with_parent(G, root)
    all_edges = {tuple(sorted(e)) for e in G.edges()}
    non_tree_edges = sorted(all_edges - tree_edges)
    cycles = []
    for e in non_tree_edges:
        u, v = e
        cyc = tree_path_edges(parent, u, v) + [e]
        cyc = list(dict.fromkeys(cyc))
        cycles.append(cyc)
    return cycles


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


def wl2_colors(G: nx.Graph, rounds: int):
    nodes = list(G.nodes())
    adj = {u: set(G.neighbors(u)) for u in nodes}

    pair_color = {}
    for u in nodes:
        for v in nodes:
            if u == v:
                pair_color[(u, v)] = ("diag", G.degree(u))
            elif v in adj[u]:
                pair_color[(u, v)] = ("edge",)
            else:
                pair_color[(u, v)] = ("nonedge",)

    for _ in range(rounds):
        new_pair_color = {}
        palette = {}
        next_id = 0
        for u in nodes:
            for v in nodes:
                multiset = []
                for w in nodes:
                    multiset.append((pair_color[(u, w)], pair_color[(w, v)]))
                key = (pair_color[(u, v)], tuple(sorted(multiset, key=str)))
                if key not in palette:
                    palette[key] = next_id
                    next_id += 1
                new_pair_color[(u, v)] = palette[key]
        pair_color = new_pair_color

    vertex_sig = {}
    palette = {}
    next_id = 0
    for u in nodes:
        sig = tuple(sorted((pair_color[(u, v)] for v in nodes)))
        if sig not in palette:
            palette[sig] = next_id
            next_id += 1
        vertex_sig[u] = palette[sig]

    return vertex_sig


def edge_orbits_from_vertex_colors(G: nx.Graph, vcolor):
    orbit_index = {}
    e_orbit = {}
    next_id = 0
    for u, v in G.edges():
        key = tuple(sorted((vcolor[u], vcolor[v])))
        if key not in orbit_index:
            orbit_index[key] = next_id
            next_id += 1
        e_orbit[tuple(sorted((u, v)))] = orbit_index[key]
    return e_orbit, orbit_index


def compressed_cycle_matrix(G: nx.Graph, cycles, wl_rounds: int):
    vcolor = wl2_colors(G, wl_rounds)
    e_orbit, e_orbit_index = edge_orbits_from_vertex_colors(G, vcolor)

    row_orbit_index = {}
    rows = []
    next_row = 0

    for cyc in cycles:
        rsig = tuple(sorted(e_orbit[tuple(sorted(e))] for e in cyc))
        if rsig not in row_orbit_index:
            row_orbit_index[rsig] = next_row
            next_row += 1
            row = np.zeros(len(e_orbit_index), dtype=np.uint8)
            for e in cyc:
                row[e_orbit[tuple(sorted(e))]] ^= 1
            rows.append(row)

    if rows:
        M = np.vstack(rows)
    else:
        M = np.zeros((0, len(e_orbit_index)), dtype=np.uint8)

    vertex_orbit_count = len(set(vcolor.values()))
    return M, vertex_orbit_count, len(e_orbit_index), len(row_orbit_index)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="family", required=True)

    ap_rr = sub.add_parser("rr")
    ap_rr.add_argument("--n", type=int, required=True)
    ap_rr.add_argument("--d", type=int, default=4)
    ap_rr.add_argument("--seed", type=int, default=0)
    ap_rr.add_argument("--wl-rounds", type=int, default=2)
    ap_rr.add_argument("--out", required=True)

    ap_lift = sub.add_parser("liftk4")
    ap_lift.add_argument("--p", type=int, required=True)
    ap_lift.add_argument("--seed", type=int, default=0)
    ap_lift.add_argument("--wl-rounds", type=int, default=2)
    ap_lift.add_argument("--out", required=True)

    args = ap.parse_args()

    if args.family == "rr":
        G = random_regular_graph(args.n, args.d, args.seed)
        meta = {"family": "random_regular", "n": args.n, "d": args.d, "seed": args.seed}
    else:
        G = random_lift_k4(args.p, args.seed)
        meta = {"family": "random_lift_K4", "p": args.p, "seed": args.seed}

    root = next(iter(G.nodes()))
    cycles = fundamental_cycles(G, root)
    M_full = incidence_matrix(G, cycles)
    M_comp, v_orbits, e_orbits, c_orbits = compressed_cycle_matrix(G, cycles, args.wl_rounds)

    out = {
        **meta,
        "graph_n": G.number_of_nodes(),
        "graph_m": G.number_of_edges(),
        "wl_rounds": args.wl_rounds,
        "fundamental_cycles": len(cycles),
        "cycle_space_dimension_exact": G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G),
        "full_rank_F2": rank_f2(M_full),
        "vertex_wl2_orbit_count": v_orbits,
        "edge_wl2_orbit_count": e_orbits,
        "cycle_wl2_orbit_count": c_orbits,
        "compressed_rank_F2": rank_f2(M_comp),
        "compressed_shape": list(M_comp.shape),
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
