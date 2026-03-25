import networkx as nx
from toolkit.oblivion.cycle_overlap_rank import overlap_rank_proxy

def expander_growth(n_values=(40,60,80,120), d=3, R=3, trials=5):
    results = []
    for n in n_values:
        vals = []
        for _ in range(trials):
            G = nx.random_regular_graph(d, n)
            vals.append(overlap_rank_proxy(G, R))
        avg = sum(vals)/len(vals)
        results.append((n, avg))
    return results

if __name__ == "__main__":
    out = expander_growth()
    for n,val in out:
        print(n,val)
