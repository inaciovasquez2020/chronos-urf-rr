import networkx as nx

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_rank_edge_addition():
    G = nx.path_graph(10)
    r1 = cycle_rank(G)
    G.add_edge(0,9)
    r2 = cycle_rank(G)
    assert r2 == r1 + 1
