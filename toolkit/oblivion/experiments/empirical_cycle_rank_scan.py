import networkx as nx
from toolkit.oblivion.cycle_overlap_rank import overlap_rank_proxy

def scan(n=100, d=3, R_values=range(1,10), trials=5):
    results = []
    for R in R_values:
        vals = []
        for _ in range(trials):
            G = nx.random_regular_graph(d, n)
            vals.append(overlap_rank_proxy(G, R))
        results.append((R, sum(vals)/len(vals)))
    return results

if __name__ == "__main__":
    out = scan()
    for R,val in out:
        print(R,val)
