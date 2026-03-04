import networkx as nx
import numpy as np

def gf2_rank(A: np.ndarray) -> int:
    A = (A.copy() % 2).astype(np.uint8)
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i, c]:
                piv = i
                break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return r

def edge_index(G: nx.Graph):
    edges = list(G.edges())
    idx = {e:i for i,e in enumerate(edges)}
    idx.update({(v,u):i for (u,v),i in idx.items()})
    return edges, idx

def cycle_space_rank(G: nx.Graph) -> int:
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def cycles_in_ball(G: nx.Graph, center, R: int):
    nodes = list(nx.single_source_shortest_path_length(G, center, cutoff=R).keys())
    H = G.subgraph(nodes).copy()
    return H

def ball_cycle_vectors(G: nx.Graph, R: int):
    edges, idx = edge_index(G)
    vecs = []
    for v in G.nodes():
        H = cycles_in_ball(G, v, R)
        # cycle basis over subgraph; each cycle is list of nodes
        for cyc in nx.cycle_basis(H):
            w = np.zeros((len(edges),), dtype=np.uint8)
            # convert node-cycle to edge set
            for i in range(len(cyc)):
                a = cyc[i]
                b = cyc[(i+1) % len(cyc)]
                w[idx[(a,b)]] ^= 1
            vecs.append(w)
    if not vecs:
        return np.zeros((0, G.number_of_edges()), dtype=np.uint8)
    return np.stack(vecs, axis=0)

def local_cycle_rank(G: nx.Graph, R: int) -> int:
    M = ball_cycle_vectors(G, R)
    return gf2_rank(M)

def overlap_rank_proxy(G: nx.Graph, R: int) -> int:
    # proxy: rank of locally-supported cycles; monotone lower bound on any overlap-rank definition
    return local_cycle_rank(G, R)
