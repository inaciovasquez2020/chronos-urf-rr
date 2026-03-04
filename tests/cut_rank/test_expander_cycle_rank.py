import networkx as nx

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_rank_expander():
    G = nx.random_regular_graph(d=3, n=50)
    assert cycle_rank(G) >= 1
