from collections import defaultdict, deque
from dataclasses import dataclass
import itertools
import sys

@dataclass
class Graph:
    adj: dict

    def add_edge(self, u, v):
        self.adj.setdefault(u, set()).add(v)
        self.adj.setdefault(v, set()).add(u)

    def vertices(self):
        return list(self.adj.keys())

    def edges(self):
        seen = set()
        out = []
        for u, nbrs in self.adj.items():
            for v in nbrs:
                e = tuple(sorted((u, v)))
                if e not in seen:
                    seen.add(e)
                    out.append(e)
        return out

def make_parallel_bundle_candidate(R: int = 2, m: int = 5):
    G = Graph(adj={})
    L = 2 * R + 2
    u, v = "u", "v"

    for i in range(m):
        prev = u
        for j in range(1, L):
            x = f"p{i}_{j}"
            G.add_edge(prev, x)
            prev = x
        G.add_edge(prev, v)

    x, a, b, c = "x", "a", "b", "c"
    K4 = [x, a, b, c]
    for s, t in itertools.combinations(K4, 2):
        G.add_edge(s, t)
    G.add_edge(u, x)

    return G

def gf2_rank(rows, ncols):
    rows = [r for r in rows if r]
    rank = 0
    col = 0
    while col < ncols and rank < len(rows):
        pivot = None
        for i in range(rank, len(rows)):
            if (rows[i] >> col) & 1:
                pivot = i
                break
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
        col += 1
    return rank

def connected_components(G: Graph):
    seen = set()
    comps = []
    for s in G.vertices():
        if s in seen:
            continue
        comp = set([s])
        q = [s]
        seen.add(s)
        while q:
            u = q.pop()
            for v in G.adj[u]:
                if v not in seen:
                    seen.add(v)
                    comp.add(v)
                    q.append(v)
        comps.append(comp)
    return comps

def betti_1(G: Graph):
    return len(G.edges()) - len(G.vertices()) + len(connected_components(G))

def all_simple_cycles_up_to_length(G: Graph, max_len: int):
    V = sorted(G.vertices())
    index = {v: i for i, v in enumerate(V)}
    cycles = set()

    def canon(cyc):
        cyc = list(cyc)
        rots = []
        n = len(cyc)
        for s in range(n):
            rots.append(tuple(cyc[s:] + cyc[:s]))
        rc = list(reversed(cyc))
        for s in range(n):
            rots.append(tuple(rc[s:] + rc[:s]))
        return min(rots)

    for start in V:
        stack = [(start, [start], {start})]
        while stack:
            u, path, used = stack.pop()
            if len(path) > max_len:
                continue
            for w in G.adj[u]:
                if w == start and len(path) >= 3:
                    cyc = canon(path[:])
                    cycles.add(cyc)
                elif index[w] >= index[start] and w not in used and len(path) < max_len:
                    stack.append((w, path + [w], used | {w}))
    return sorted(cycles)

def cycle_to_row(cycle, edge_index):
    row = 0
    n = len(cycle)
    for i in range(n):
        a = cycle[i]
        b = cycle[(i + 1) % n]
        e = tuple(sorted((a, b)))
        row ^= (1 << edge_index[e])
    return row

def short_cycle_span_rank(G: Graph, cutoff: int):
    edges = G.edges()
    edge_index = {e: i for i, e in enumerate(edges)}
    cycles = all_simple_cycles_up_to_length(G, cutoff)
    rows = [cycle_to_row(c, edge_index) for c in cycles]
    return gf2_rank(rows, len(edges)), len(cycles)

def main():
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    G = make_parallel_bundle_candidate(R=R, m=m)
    beta = betti_1(G)
    cutoff = 2 * R + 1
    short_rank, short_count = short_cycle_span_rank(G, cutoff)
    quotient = beta - short_rank

    print(f"R: {R}")
    print(f"m_parallel_paths: {m}")
    print(f"vertices: {len(G.vertices())}")
    print(f"edges: {len(G.edges())}")
    print(f"beta_1_total: {beta}")
    print(f"short_cycle_cutoff: {cutoff}")
    print(f"enumerated_short_cycles: {short_count}")
    print(f"short_cycle_span_rank: {short_rank}")
    print(f"exact_quotient_rank: {quotient}")

    assert quotient >= 4, f"expected quotient >= 4, got {quotient}"

if __name__ == "__main__":
    main()
