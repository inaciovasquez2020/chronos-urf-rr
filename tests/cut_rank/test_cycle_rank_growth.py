import networkx as nx

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_rank_positive_on_cycle():
    G = nx.cycle_graph(10)
    assert cycle_rank(G) > 0
