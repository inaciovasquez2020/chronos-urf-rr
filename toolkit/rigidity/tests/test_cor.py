import networkx as nx
from toolkit.rigidity.scripts.cycle_overlap_rank import cycle_overlap_rank

def test_small_cycle():
    G = nx.cycle_graph(6)
    cor = cycle_overlap_rank(G)
    assert cor >= 1

def test_tree():
    G = nx.path_graph(10)
    cor = cycle_overlap_rank(G)
    assert cor == 0
