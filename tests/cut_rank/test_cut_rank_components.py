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

def test_cut_rank_components():
    G1 = nx.cycle_graph(5)
    G2 = nx.path_graph(4)
    G = nx.disjoint_union(G1, G2)
    B = incidence_matrix(G)
    assert gf2_rank(B) == G.number_of_nodes() - nx.number_connected_components(G)
