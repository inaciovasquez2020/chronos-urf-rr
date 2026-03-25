import networkx as nx
import numpy as np

def incidence_matrix(G):
    nodes = list(G.nodes())
    edges = list(G.edges())
    B = np.zeros((len(nodes), len(edges)), dtype=int)
    for j,(u,v) in enumerate(edges):
        B[nodes.index(u), j] = 1
        B[nodes.index(v), j] = 1
    return B % 2

def gf2_rank(M):
    M = M.copy()
    r = 0
    for c in range(M.shape[1]):
        pivot = None
        for i in range(r, M.shape[0]):
            if M[i,c]:
                pivot = i
                break
        if pivot is None:
            continue
        M[[r,pivot]] = M[[pivot,r]]
        for i in range(M.shape[0]):
            if i != r and M[i,c]:
                M[i] ^= M[r]
        r += 1
    return r

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_cut_rank_general_graph():
    G = nx.gnm_random_graph(30, 60)
    B = incidence_matrix(G)
    cut_rank = gf2_rank(B)
    c_rank = cycle_rank(G)
    assert cut_rank + c_rank == G.number_of_edges()
