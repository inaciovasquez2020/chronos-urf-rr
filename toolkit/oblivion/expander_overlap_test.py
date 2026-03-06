import networkx as nx
import random
import json

def local_cycles_edgevecs(G, v, R, edge_index):
    B = nx.ego_graph(G, v, radius=R)
    vecs = []
    for cyc in nx.cycle_basis(B):
        vec = [0] * len(edge_index)
        for i in range(len(cyc)):
            a = cyc[i]
            b = cyc[(i + 1) % len(cyc)]
            e = tuple(sorted((a, b)))
            j = edge_index.get(e)
            if j is not None:
                vec[j] ^= 1
        if any(vec):
            vecs.append(vec)
    return vecs

def gf2_rank(vectors, m):
    basis = {}
    rank = 0
    for v in vectors:
        x = v[:]
        while True:
            try:
                p = x.index(1)
            except ValueError:
                break
            b = basis.get(p)
            if b is None:
                basis[p] = x
                rank += 1
                break
            for j in range(m):
                x[j] ^= b[j]
    return rank

def cycle_overlap_rank(G, R):
    edge_index = {tuple(sorted(e)): i for i, e in enumerate(G.edges())}
    m = len(edge_index)
    vecs = []
    for v in G.nodes():
        vecs.extend(local_cycles_edgevecs(G, v, R, edge_index))
    return gf2_rank(vecs, m)

def wl_hash_ball(G, v, r):
    import networkx.algorithms.graph_hashing as gh
    B = nx.ego_graph(G, v, radius=r)
    return gh.weisfeiler_lehman_graph_hash(B)

def fo_type_diversity(G, r):
    types = set()
    for v in G.nodes():
        types.add(wl_hash_ball(G, v, r))
    return len(types)

def expander_blocks(k, m, d_block, p_bridge, seed):
    random.seed(seed)
    blocks = [nx.random_regular_graph(d_block, m, seed=seed + i) for i in range(k)]
    G = nx.Graph()
    offset = 0
    block_nodes = []
    for B in blocks:
        mapping = {v: v + offset for v in B.nodes()}
        B2 = nx.relabel_nodes(B, mapping)
        G = nx.compose(G, B2)
        block_nodes.append(list(mapping.values()))
        offset += m

    # sparse expander-like bridge pattern over k blocks
    for i in range(k):
        for j in range(i + 1, k):
            if random.random() < p_bridge:
                u = random.choice(block_nodes[i])
                v = random.choice(block_nodes[j])
                G.add_edge(u, v)
    return G

def run(trials=10, k=10, m=40, d_block=3, p_bridge=0.30, R=2, r=2, seed=0):
    out = []
    for t in range(trials):
        G = expander_blocks(k, m, d_block, p_bridge, seed + 1000 * t)
        C = cycle_overlap_rank(G, R)
        T = fo_type_diversity(G, r)
        out.append({
            "trial": t,
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "C_R": C,
            "T_r": T,
            "C_over_V": C / G.number_of_nodes(),
            "C_over_E": C / G.number_of_edges(),
            "params": {"k": k, "m": m, "d_block": d_block, "p_bridge": p_bridge, "R": R, "r": r}
        })
    return out

if __name__ == "__main__":
    results = run()
    print(json.dumps(results, indent=2))
