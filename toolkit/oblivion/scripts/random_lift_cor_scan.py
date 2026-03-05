# toolkit/oblivion/scripts/random_lift_cor_scan.py

from __future__ import annotations
import argparse, json, random, time
from typing import Dict, List, Tuple, Set
import numpy as np
import networkx as nx

from toolkit.oblivion.scripts.gf2_csr import build_incidence_gf2_csr, GF2CSR


def load_graph_json(path: str) -> nx.Graph:
    with open(path, "r") as f:
        obj = json.load(f)
    G = nx.Graph()
    if "edges" in obj:
        G.add_edges_from((int(u), int(v)) for u, v in obj["edges"])
    elif "adj" in obj:
        for u, nbrs in obj["adj"].items():
            u = int(u)
            for v in nbrs:
                G.add_edge(u, int(v))
    else:
        raise ValueError("graph_json must contain either 'edges' or 'adj'")
    return G


def random_lift(base: nx.Graph, n: int, seed: int) -> nx.Graph:
    rng = random.Random(seed)
    G = nx.Graph()
    base_nodes = list(base.nodes())
    for u in base_nodes:
        for i in range(n):
            G.add_node((u, i))
    for (u, v) in base.edges():
        perm = list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            G.add_edge((u, i), (v, perm[i]))
    return G


def bfs_cycle(G: nx.Graph, start, L: int):
    import collections
    visited = {start: None}
    depth = {start: 0}
    q = collections.deque([start])
    while q:
        x = q.popleft()
        if depth[x] >= L:
            continue
        for y in G[x]:
            if y not in visited:
                visited[y] = x
                depth[y] = depth[x] + 1
                q.append(y)
            elif visited[x] != y:
                cyc = [x]
                t = x
                while t != y and t is not None:
                    t = visited[t]
                    cyc.append(t)
                if cyc[-1] is None:
                    continue
                return cyc
    return None


def cycle_edges_from_nodes(cycle_nodes: List) -> Set[Tuple]:
    es = set()
    for i in range(len(cycle_nodes) - 1):
        a, b = cycle_nodes[i], cycle_nodes[i + 1]
        es.add((a, b) if a <= b else (b, a))
    return es


def pack_cycles_bfs(G: nx.Graph, L: int, target: int, seed: int, vertex_sample: int):
    rng = random.Random(seed)
    nodes = list(G.nodes())
    if vertex_sample < len(nodes):
        nodes = rng.sample(nodes, vertex_sample)
    H = G.copy()
    cycles = []
    for v in nodes:
        if len(cycles) >= target:
            break
        if v not in H:
            continue
        c = bfs_cycle(H, v, L)
        if c is None:
            continue
        if len(c) < 3:
            continue
        es = cycle_edges_from_nodes(c)
        if not es:
            continue
        cycles.append((v, es, c))
        H.remove_edges_from(list(es))
    return cycles


def cor_lower_bound_from_cycles(cycles) -> int:
    return len(cycles)


def build_cycle_patch_incidence_lb(cycles, n_patches: int):
    # Lower-bound incidence: each cycle assigned to its chosen center patch index
    ones = []
    for i, (center, es, nodes) in enumerate(cycles):
        ones.append((i, i if i < n_patches else (i % n_patches)))
    return ones


def wiedemann_block_krylov_rank_lb(A: GF2CSR, block: int, steps: int, trials: int, seed: int) -> int:
    rng = np.random.default_rng(seed)
    n = A.shape[1]
    best = 0
    for t in range(trials):
        V = rng.integers(0, 2, size=(n, block), dtype=np.uint8)
        cols = []
        X = V
        for _ in range(steps):
            cols.append(X)
            X = A.mm(X)
        K = np.concatenate(cols, axis=1)  # n x (block*steps)
        rank_lb = int(np.linalg.matrix_rank(K % 2))
        best = max(best, rank_lb)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_json", required=True)
    ap.add_argument("--lift_n", type=int, required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--R", type=int, default=6)
    ap.add_argument("--L", type=int, default=12)  # use L <= 2R
    ap.add_argument("--target_cycles", type=int, default=5000)
    ap.add_argument("--vertex_sample", type=int, default=60000)
    ap.add_argument("--rank_trials", type=int, default=3)
    ap.add_argument("--rank_block", type=int, default=16)
    ap.add_argument("--rank_steps", type=int, default=64)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    t0 = time.time()
    base = load_graph_json(args.base_json)
    G = random_lift(base, args.lift_n, args.seed)
    t1 = time.time()

    cycles = pack_cycles_bfs(G, L=args.L, target=args.target_cycles, seed=args.seed, vertex_sample=args.vertex_sample)
    cor_lb = cor_lower_bound_from_cycles(cycles)
    t2 = time.time()

    # Optional: build a sparse incidence matrix and get a rank lower bound (still a lower bound here)
    ones = build_cycle_patch_incidence_lb(cycles, n_patches=cor_lb if cor_lb > 0 else 1)
    A = build_incidence_gf2_csr(n_rows=max(1, cor_lb), n_cols=max(1, cor_lb), ones=ones)
    rank_lb = wiedemann_block_krylov_rank_lb(
        A, block=args.rank_block, steps=args.rank_steps, trials=args.rank_trials, seed=args.seed + 1337
    )
    t3 = time.time()

    out = {
        "meta": {
            "base_json": args.base_json,
            "lift_n": args.lift_n,
            "seed": args.seed,
            "R": args.R,
            "L": args.L,
            "target_cycles": args.target_cycles,
            "vertex_sample": args.vertex_sample,
            "rank_trials": args.rank_trials,
            "rank_block": args.rank_block,
            "rank_steps": args.rank_steps,
        },
        "timing_sec": {
            "lift": round(t1 - t0, 6),
            "cycle_packing": round(t2 - t1, 6),
            "rank_lb": round(t3 - t2, 6),
        },
        "cycle_packing": {
            "packed_cycles": cor_lb,
            "cor_lb_from_packing": cor_lb,
            "rank_lb_incidence": int(rank_lb),
        },
    }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
