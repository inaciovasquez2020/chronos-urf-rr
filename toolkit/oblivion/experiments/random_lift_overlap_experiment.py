import networkx as nx
from toolkit.oblivion.cycle_overlap_rank import overlap_rank_proxy

def random_lift_overlap(base_nodes=6, lift=20, R=3, trials=5):
    base = nx.cycle_graph(base_nodes)
    results = []
    for _ in range(trials):
        G = nx.random_lift(base, lift)
        r = overlap_rank_proxy(G, R)
        results.append(r)
    return results

if __name__ == "__main__":
    vals = random_lift_overlap()
    for v in vals:
        print(v)
