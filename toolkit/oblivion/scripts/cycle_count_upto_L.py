import networkx as nx
import argparse
import json
from collections import defaultdict, deque

def ball_edges_upper_bound(delta: int, R: int) -> int:
    if R <= 0:
        return 0
    if delta <= 1:
        return 0
    # nodes in ball: 1 + Δ * sum_{i=0}^{R-1} (Δ-1)^i
    nodes = 1 + delta * sum((delta - 1) ** i for i in range(R))
    # edges <= Δ/2 * |V|
    return int((delta * nodes) // 2)

def canonical_cycle(nodes):
    # nodes is a list representing a cycle in order (start repeated not included)
    m = len(nodes)
    # rotate to minimal tuple among all rotations, and also for reversed
    rots = [tuple(nodes[i:] + nodes[:i]) for i in range(m)]
    rnodes = list(reversed(nodes))
    rrots = [tuple(rnodes[i:] + rnodes[:i]) for i in range(m)]
    return min(rots + rrots)

def count_simple_cycles_upto_L(G: nx.Graph, L: int):
    # Enumerate all simple cycles up to length L in an undirected graph
    # using start-node ordering to avoid duplicates.
    nodes = sorted(G.nodes())
    index = {v: i for i, v in enumerate(nodes)}
    seen = set()
    counts = defaultdict(int)

    for s in nodes:
        s_idx = index[s]
        stack = [(s, [s], set([s]))]

        while stack:
            u, path, used = stack.pop()
            if len(path) > L:
                continue
            for w in G.neighbors(u):
                w_idx = index[w]
                if w == s and len(path) >= 3:
                    cyc = canonical_cycle(path[:])
                    if cyc not in seen:
                        seen.add(cyc)
                        counts[len(cyc)] += 1
                    continue
                if w in used:
                    continue
                # enforce canonical start: only visit nodes with index >= s_idx
                if w_idx < s_idx:
                    continue
                stack.append((w, path + [w], used | {w}))

    total = sum(counts.values())
    return total, dict(sorted(counts.items()))

def build_torus(n: int) -> nx.Graph:
    G = nx.Graph()
    for i in range(n):
        for j in range(n):
            v = (i, j)
            G.add_edge(v, ((i + 1) % n, j))
            G.add_edge(v, (i, (j + 1) % n))
    return G

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", choices=["random_regular", "torus"], required=True)
    ap.add_argument("--n", type=int, required=True, help="random_regular: number of vertices; torus: side length")
    ap.add_argument("--d", type=int, default=3, help="degree for random_regular")
    ap.add_argument("--R", type=int, default=2, help="radius used only to compute default L")
    ap.add_argument("--L", type=int, default=None, help="override max cycle length")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    if args.graph == "random_regular":
        G = nx.random_regular_graph(args.d, args.n, seed=args.seed)
        delta = args.d
        n_vertices = args.n
    else:
        G = build_torus(args.n)
        delta = 4
        n_vertices = args.n * args.n

    L = args.L if args.L is not None else ball_edges_upper_bound(delta, args.R)

    total, by_len = count_simple_cycles_upto_L(G, L)

    result = {
        "graph": args.graph,
        "n_param": args.n,
        "vertices": n_vertices,
        "degree": delta,
        "R": args.R,
        "L_max": L,
        "num_simple_cycles_upto_L": total,
        "num_simple_cycles_by_length": by_len,
    }

    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
