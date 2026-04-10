from collections import deque
from itertools import combinations
import json

R = 2

def construct_base_heawood():
    adj = {
        0: [1, 5, 13],
        1: [0, 2, 10],
        2: [1, 3, 7],
        3: [2, 4, 12],
        4: [3, 5, 9],
        5: [0, 4, 6],
        6: [5, 7, 11],
        7: [2, 6, 8],
        8: [7, 9, 13],
        9: [4, 8, 10],
        10: [1, 9, 11],
        11: [6, 10, 12],
        12: [3, 11, 13],
        13: [0, 8, 12],
    }
    return {k: sorted(v) for k, v in adj.items()}

def edge_list(adj):
    out = []
    for u in sorted(adj):
        for v in adj[u]:
            if u < v:
                out.append((u, v))
    return out

def generate_lift(base_adj, twisted_edge=None):
    n = len(base_adj)
    lift_adj = { (u,b): set() for u in range(n) for b in (0,1) }
    for u, v in edge_list(base_adj):
        sigma = 1 if twisted_edge is not None and tuple(sorted((u, v))) == tuple(sorted(twisted_edge)) else 0
        for b in (0,1):
            x = (u, b)
            y = (v, b ^ sigma)
            lift_adj[x].add(y)
            lift_adj[y].add(x)
    return {k: sorted(v) for k, v in lift_adj.items()}

def canonical_pairing(base_adj):
    n = len(base_adj)
    return {(u, b): (u, b) for u in range(n) for b in (0,1)}

def ball_vertices(adj, root, radius):
    dist = {root: 0}
    q = deque([root])
    while q:
        u = q.popleft()
        if dist[u] == radius:
            continue
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist

def induced_subgraph(adj, verts):
    s = set(verts)
    return {u: sorted(v for v in adj[u] if v in s) for u in verts}

def base_projection_ball(base_adj, root_u, radius):
    dist = {root_u: 0}
    q = deque([root_u])
    while q:
        u = q.popleft()
        if dist[u] == radius:
            continue
        for w in base_adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist

def gauge_from_tree(base_adj, twisted_edge, root_u, radius):
    ball = base_projection_ball(base_adj, root_u, radius)
    parent = {root_u: None}
    q = deque([root_u])
    while q:
        u = q.popleft()
        if ball[u] == radius:
            continue
        for w in base_adj[u]:
            if w in ball and w not in parent:
                parent[w] = u
                q.append(w)
    tau = {root_u: 0}
    order = [root_u]
    q = deque([root_u])
    while q:
        u = q.popleft()
        for w in base_adj[u]:
            if w in ball and parent.get(w) == u:
                e = tuple(sorted((u, w)))
                sigma = 1 if twisted_edge is not None and e == tuple(sorted(twisted_edge)) else 0
                tau[w] = tau[u] ^ sigma
                q.append(w)
                order.append(w)
    return tau

def certify_ball_isomorphism(base_adj, g_plus, g_minus, pairing, twisted_edge, radius=2):
    certs = []
    all_ok = True
    for root_plus, root_minus in sorted(pairing.items()):
        u, b = root_plus
        ball_plus_dist = ball_vertices(g_plus, root_plus, radius)
        ball_minus_dist = ball_vertices(g_minus, root_minus, radius)

        tau = gauge_from_tree(base_adj, twisted_edge, u, radius)

        image = {}
        for (x, bx), d in ball_plus_dist.items():
            image[(x, bx)] = (x, bx ^ tau[x])

        image_set = set(image.values())
        ok_vertices = image_set == set(ball_minus_dist.keys())

        ok_root = image[root_plus] == root_minus

        ok_distance = True
        for v, img in image.items():
            if ball_plus_dist[v] != ball_minus_dist[img]:
                ok_distance = False
                break

        ok_edges = True
        for v in ball_plus_dist:
            lhs = {image[w] for w in g_plus[v] if w in ball_plus_dist}
            rhs = set(w for w in g_minus[image[v]] if w in ball_minus_dist)
            if lhs != rhs:
                ok_edges = False
                break

        ok = ok_vertices and ok_root and ok_distance and ok_edges
        all_ok = all_ok and ok
        certs.append({
            "root_plus": list(root_plus),
            "root_minus": list(root_minus),
            "ok_vertices": ok_vertices,
            "ok_root": ok_root,
            "ok_distance": ok_distance,
            "ok_edges": ok_edges,
            "isomorphic": ok,
            "tau_support": sorted([x for x, t in tau.items() if t == 1]),
        })
    return {
        "radius": radius,
        "twisted_edge": list(twisted_edge) if twisted_edge is not None else None,
        "all_roots_isomorphic": all_ok,
        "certificates": certs,
    }

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

def graph_edge_index(adj):
    idx = {}
    edges = []
    k = 0
    for u in sorted(adj):
        for v in adj[u]:
            if u < v:
                idx[(u, v)] = k
                edges.append((u, v))
                k += 1
    return idx, edges

def all_simple_cycles_up_to_length(adj, max_len):
    cycles = set()
    vertices = sorted(adj)

    def canonicalize(cyc):
        cyc = list(cyc)
        rots = []
        n = len(cyc)
        for i in range(n):
            rots.append(tuple(cyc[i:] + cyc[:i]))
        rc = list(reversed(cyc))
        for i in range(n):
            rots.append(tuple(rc[i:] + rc[:i]))
        return min(rots)

    for s in vertices:
        stack = [(s, [s], {s})]
        while stack:
            u, path, seen = stack.pop()
            if len(path) > max_len:
                continue
            for w in adj[u]:
                if w == s and len(path) >= 3:
                    cyc = canonicalize(path[:])
                    if len(cyc) <= max_len:
                        cycles.add(cyc)
                elif w not in seen and w >= s:
                    stack.append((w, path + [w], seen | {w}))
    return sorted(cycles)

def cycle_to_bitrow(cycle, edge_idx):
    bits = 0
    n = len(cycle)
    for i in range(n):
        a = cycle[i]
        b = cycle[(i + 1) % n]
        e = tuple(sorted((a, b)))
        bits |= (1 << edge_idx[e])
    return bits

def compute_urf_invariant(adj, radius=2):
    edge_idx, edges = graph_edge_index(adj)
    ncols = len(edges)
    local_bound = 2 * radius + 1

    all_cycles = all_simple_cycles_up_to_length(adj, max_len=len(adj))
    local_cycles = [c for c in all_cycles if len(c) <= local_bound]

    all_rows = [cycle_to_bitrow(c, edge_idx) for c in all_cycles]
    local_rows = [cycle_to_bitrow(c, edge_idx) for c in local_cycles]

    z1_dim = gf2_rank(all_rows, ncols)
    local_dim = gf2_rank(local_rows, ncols)
    urf = z1_dim - local_dim

    return {
        "num_vertices": len(adj),
        "num_edges": len(edges),
        "z1_dimension": z1_dim,
        "local_cycle_span_dimension": local_dim,
        "urf_invariant": urf,
        "num_cycles_total": len(all_cycles),
        "num_cycles_local": len(local_cycles),
        "local_cycle_length_bound": local_bound,
    }

def serialize_lift(adj):
    out = {}
    for (u, b), nbrs in sorted(adj.items()):
        out[f"{u}_{b}"] = [f"{x}_{y}" for (x, y) in nbrs]
    return out

def main():
    base = construct_base_heawood()
    twisted_edge = (0, 1)

    g_plus = generate_lift(base, twisted_edge=None)
    g_minus = generate_lift(base, twisted_edge=twisted_edge)
    pairing = canonical_pairing(base)

    cert = certify_ball_isomorphism(base, g_plus, g_minus, pairing, twisted_edge, radius=R)
    inv_plus = compute_urf_invariant(g_plus, radius=R)
    inv_minus = compute_urf_invariant(g_minus, radius=R)

    out = {
        "base_name": "HeawoodGraph",
        "radius": R,
        "base_girth": 6,
        "twisted_edge": list(twisted_edge),
        "pairing": {f"{u}_{b}": f"{x}_{y}" for (u, b), (x, y) in sorted(pairing.items())},
        "local_certificate": cert,
        "G_plus": inv_plus,
        "G_minus": inv_minus,
        "lift_plus_adj": serialize_lift(g_plus),
        "lift_minus_adj": serialize_lift(g_minus),
    }

    with open("artifacts/heawood_lift_pair_r2.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

if __name__ == "__main__":
    main()
