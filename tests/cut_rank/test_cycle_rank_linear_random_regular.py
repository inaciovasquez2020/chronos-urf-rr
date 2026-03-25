import networkx as nx

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_rank_linear_random_regular():
    n = 60
    d = 3
    G = nx.random_regular_graph(d, n)
    r = cycle_rank(G)
    assert r >= n//4
