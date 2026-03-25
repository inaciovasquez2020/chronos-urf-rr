import networkx as nx
import matplotlib.pyplot as plt
from toolkit.oblivion.cycle_overlap_rank import overlap_rank_proxy

def visualize(n_values=(30,50,80,120), d=3, R=3, trials=5):
    xs = []
    ys = []
    for n in n_values:
        vals = []
        for _ in range(trials):
            G = nx.random_regular_graph(d, n)
            vals.append(overlap_rank_proxy(G, R))
        xs.append(n)
        ys.append(sum(vals)/len(vals))
    plt.plot(xs, ys, marker="o")
    plt.xlabel("graph size n")
    plt.ylabel("avg overlap rank proxy")
    plt.title("Cycle-overlap growth")
    plt.show()

if __name__ == "__main__":
    visualize()
