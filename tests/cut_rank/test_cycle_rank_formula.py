import networkx as nx

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_rank_complete_graph():
    G = nx.complete_graph(6)
    expected = G.number_of_edges() - G.number_of_nodes() + 1
    assert cycle_rank(G) == expected
