#!/usr/bin/env python3
import argparse
import json
from collections import deque

import networkx as nx
import numpy as np


def cfi_base_cycle(m: int) -> nx.Graph:
    return nx.cycle_graph(m)


def cfi_proxy_lift(base: nx.Graph) -> nx.Graph:
    G = nx.Graph()
    for v in base.nodes():
        G.add_node((v, 0))
        G.add_node((v, 1))
    for u, v in base.edges():
        G.add_edge((u, 0), (v, 0))
        G.add_edge((u, 1), (v, 1))
        G.add_edge((u, 0), (v, 1))
        G.add_edge((u, 1), (v, 0))
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


def wl1_colors(G: nx.Graph, rounds: int):
    color = {v: G.degree(v) for v in G.nodes()}
    for _ in range(rounds):
        palette = {}
        next_id = 0
        new_color = {}
        for v in G.nodes():
            key = (color[v], tuple(sorted(color[w] for w in G.neighbors(v))))
            if key not in palette:
                palette[key] = next_id
                next_id += 1
            new_color[v] = palette[key]
        color = new_color
    return color


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


def compressed_cycle_matrix(G: nx.Graph, cycles, rounds: int):
    vcolor = wl1_colors(G, rounds)
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
    return M, len(set(vcolor.values())), len(e_orbit_index), len(row_orbit_index)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=40)
    ap.add_argument("--wl-rounds", type=int, default=3)
    ap.add_argument("--out", default="toolkit/oblivion/results/cfi_homogeneous_proxy.json")
    args = ap.parse_args()

    base = cfi_base_cycle(args.m)
    G = cfi_proxy_lift(base)
    root = next(iter(G.nodes()))
    cycles = fundamental_cycles(G, root)
    M_full = incidence_matrix(G, cycles)
    M_comp, v_orbits, e_orbits, c_orbits = compressed_cycle_matrix(G, cycles, args.wl_rounds)

    out = {
        "family": "cfi_proxy_cycle_lift",
        "m": args.m,
        "graph_n": G.number_of_nodes(),
        "graph_m": G.number_of_edges(),
        "wl_rounds": args.wl_rounds,
        "fundamental_cycles": len(cycles),
        "cycle_space_dimension_exact": G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G),
        "full_rank_F2": rank_f2(M_full),
        "vertex_wl1_orbit_count": v_orbits,
        "edge_wl1_orbit_count": e_orbits,
        "cycle_wl1_orbit_count": c_orbits,
        "compressed_rank_F2": rank_f2(M_comp),
        "compressed_shape": list(M_comp.shape),
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
