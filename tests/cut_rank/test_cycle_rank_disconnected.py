import networkx as nx

def cycle_rank(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)

def test_cycle_rank_disconnected_union():
    G1 = nx.cycle_graph(6)
    G2 = nx.cycle_graph(8)
    G = nx.disjoint_union(G1, G2)
    assert cycle_rank(G) == cycle_rank(G1) + cycle_rank(G2)
