import networkx as nx
from toolkit.oblivion.cycle_overlap_rank import overlap_rank_proxy, cycle_space_rank

def test_local_cycle_rank_proxy_tree_zero():
    G = nx.random_labeled_tree(40)
    assert overlap_rank_proxy(G, R=3) == 0
    assert cycle_space_rank(G) == 0

def test_local_cycle_rank_proxy_cycle_positive_when_radius_large():
    G = nx.cycle_graph(30)
    assert overlap_rank_proxy(G, R=20) >= 1

def test_local_cycle_rank_proxy_random_regular_grows():
    G = nx.random_regular_graph(d=3, n=80)
    r = overlap_rank_proxy(G, R=2)
    assert r >= 1
