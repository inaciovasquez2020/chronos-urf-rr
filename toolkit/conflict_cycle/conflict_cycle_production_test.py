import networkx as nx
import random
import numpy as np

def random_regular_expander(n, d):
    while True:
        G = nx.random_regular_graph(d, n)
        if nx.is_connected(G):
            return G

def build_expander_of_expanders(k, m, d_inner=3, d_outer=3):
    H = random_regular_expander(k, d_outer)
    blocks = []
    offset = 0
    G = nx.Graph()

    for i in range(k):
        B = random_regular_expander(m, d_inner)
        mapping = {v: v + offset for v in B.nodes()}
        B = nx.relabel_nodes(B, mapping)
        G = nx.compose(G, B)
        blocks.append(list(mapping.values()))
        offset += m

    for (i, j) in H.edges():
        u = random.choice(blocks[i])
        v = random.choice(blocks[j])
        G.add_edge(u, v)

    return G

def cycle_rank(G):
    m = G.number_of_edges()
    n = G.number_of_nodes()
    c = nx.number_connected_components(G)
    return m - n + c

def random_cut_vector(G):
    nodes = list(G.nodes())
    U = set(random.sample(nodes, len(nodes)//2))
    vec = []
    for (u,v) in G.edges():
        vec.append((u in U) ^ (v in U))
    return np.array(vec, dtype=int)

def span_rank(vectors):
    if len(vectors) == 0:
        return 0
    M = np.array(vectors) % 2
    return np.linalg.matrix_rank(M)

def simulate_clause_span(G, steps=200):
    spans = []
    vectors = []

    for _ in range(steps):
        vec = random_cut_vector(G)
        vectors.append(vec)
        spans.append(span_rank(vectors))

    return spans

if __name__ == "__main__":

    k = 10
    m = 10

    G = build_expander_of_expanders(k,m)

    print("nodes", G.number_of_nodes())
    print("edges", G.number_of_edges())
    print("cycle rank", cycle_rank(G))

    spans = simulate_clause_span(G,300)

    print("max simulated span", max(spans))
