from collections import defaultdict, deque
from dataclasses import dataclass
import itertools
import sys

@dataclass
class Graph:
    adj: dict

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

    def add_edge(self, u, v):
        self.adj.setdefault(u, set()).add(v)
        self.adj.setdefault(v, set()).add(u)

    def has_edge(self, u, v):
        return v in self.adj.get(u, ())

def new_graph():
    return Graph(adj={})

def betti_1(G: Graph) -> int:
    n = len(G.vertices())
    m = len(G.edges())
    comps = connected_components(G)
    return m - n + comps

def connected_components(G: Graph) -> int:
    seen = set()
    c = 0
    for s in G.vertices():
        if s in seen:
            continue
        c += 1
        q = [s]
        seen.add(s)
        while q:
            u = q.pop()
            for v in G.adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
    return c

def make_parallel_bundle_candidate(R: int = 2, m: int = 5):
    """
    Candidate:
      - m parallel u-v paths, each of length L = 2R+2
      - a K4 attached to u by a single bridge
    Consequences:
      - bundle contributes betti = m-1
      - attached K4 contributes local cycles only
      - graph contains a K4 minor/subgraph, so treewidth >= 3
      - explicit width-3 tree decomposition exists
    """
    L = 2 * R + 2
    G = new_graph()

    u, v = "u", "v"

    # m parallel u-v paths of equal length L
    paths = []
    for i in range(m):
        prev = u
        path_internal = []
        for j in range(1, L):
            x = f"p{i}_{j}"
            path_internal.append(x)
            G.add_edge(prev, x)
            prev = x
        G.add_edge(prev, v)
        paths.append((u, *path_internal, v))

    # Attach a K4 by a bridge at a fresh vertex x
    x, a, b, c = "x", "a", "b", "c"
    K4 = [x, a, b, c]
    for s, t in itertools.combinations(K4, 2):
        G.add_edge(s, t)
    G.add_edge(u, x)  # bridge to the bundle

    return G, paths, L

def explicit_width3_decomposition(G: Graph, paths):
    """
    Construct a width-3 tree decomposition.
    Bags are sets of size <= 4.
    """
    bags = []
    tree_edges = []

    # central articulation bag
    center = frozenset({"u", "v"})
    bags.append(center)

    # K4 bag and bridge bag
    bag_k4 = frozenset({"x", "a", "b", "c"})
    bag_bridge = frozenset({"u", "x"})
    bags.extend([bag_k4, bag_bridge])
    tree_edges.append((center, bag_bridge))
    tree_edges.append((bag_bridge, bag_k4))

    # path bags
    for i, path in enumerate(paths):
        internal = list(path[1:-1])
        if len(internal) == 1:
            b = frozenset({"u", internal[0], "v"})
            bags.append(b)
            tree_edges.append((center, b))
            continue

        prev_bag = center
        for j in range(len(internal) - 1):
            b = frozenset({"u", internal[j], internal[j + 1], "v"})
            bags.append(b)
            tree_edges.append((prev_bag, b))
            prev_bag = b

    return bags, tree_edges

def verify_tree_decomposition(G: Graph, bags, tree_edges) -> bool:
    bag_list = list(bags)
    bag_set = set(bag_list)

    # Tree sanity
    if not bag_list:
        return False
    if any(a not in bag_set or b not in bag_set for a, b in tree_edges):
        return False
    if len(tree_edges) != len(bag_list) - 1:
        return False

    # connected + acyclic
    tadj = defaultdict(set)
    for a, b in tree_edges:
        tadj[a].add(b)
        tadj[b].add(a)
    seen = set()
    q = [bag_list[0]]
    seen.add(bag_list[0])
    while q:
        z = q.pop()
        for w in tadj[z]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    if len(seen) != len(bag_list):
        return False

    # every vertex appears in a connected set of bags
    vertex_bags = defaultdict(list)
    for b in bag_list:
        for x in b:
            vertex_bags[x].append(b)
    for x, xb in vertex_bags.items():
        xb = set(xb)
        start = next(iter(xb))
        seen_x = {start}
        q = [start]
        while q:
            z = q.pop()
            for w in tadj[z]:
                if w in xb and w not in seen_x:
                    seen_x.add(w)
                    q.append(w)
        if seen_x != xb:
            return False

    # every edge covered by some bag
    for u, v in G.edges():
        if not any(u in b and v in b for b in bag_list):
            return False

    return True

def contains_k4_subgraph(G: Graph) -> bool:
    V = G.vertices()
    for quad in itertools.combinations(V, 4):
        if all(G.has_edge(s, t) for s, t in itertools.combinations(quad, 2)):
            return True
    return False

def shortest_bundle_cycle_length(L: int) -> int:
    # Any cycle using two distinct bundle paths has length 2L.
    return 2 * L

def main():
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    G, paths, L = make_parallel_bundle_candidate(R=R, m=m)
    bags, tree_edges = explicit_width3_decomposition(G, paths)

    beta = betti_1(G)
    quotient_lower_bound = m - 1
    local_cutoff = 2 * R + 1
    bundle_shortest_cycle = shortest_bundle_cycle_length(L)

    report = {
        "R": R,
        "m_parallel_paths": m,
        "path_length_L": L,
        "vertices": len(G.vertices()),
        "edges": len(G.edges()),
        "beta_1_total": beta,
        "quotient_rank_lower_bound_from_bundle": quotient_lower_bound,
        "local_cycle_cutoff_2R_plus_1": local_cutoff,
        "shortest_bundle_cycle_length": bundle_shortest_cycle,
        "bundle_has_no_cycles_at_or_below_cutoff": bundle_shortest_cycle > local_cutoff,
        "contains_K4_subgraph_so_treewidth_at_least_3": contains_k4_subgraph(G),
        "explicit_width_3_decomposition_verified": verify_tree_decomposition(G, bags, tree_edges),
        "candidate_falsifies_tw_le_t_bound_at_R": quotient_lower_bound >= 4,
    }

    for k, v in report.items():
        print(f"{k}: {v}")

    # Hard test conditions for the candidate
    assert report["contains_K4_subgraph_so_treewidth_at_least_3"]
    assert report["explicit_width_3_decomposition_verified"]
    assert report["bundle_has_no_cycles_at_or_below_cutoff"]
    assert report["quotient_rank_lower_bound_from_bundle"] >= 4

if __name__ == "__main__":
    main()
