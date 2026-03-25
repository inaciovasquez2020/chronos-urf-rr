import argparse, json, random
import networkx as nx
import numpy as np

def cycle_rank(G):
    m = G.number_of_edges()
    n = G.number_of_nodes()
    c = nx.number_connected_components(G)
    return m - n + c

def random_lift(base_n, lift_n, d):
    G = nx.random_regular_graph(d, lift_n)
    return G

parser = argparse.ArgumentParser()
parser.add_argument("--family", default="random_lifts")
parser.add_argument("--out", required=True)
args = parser.parse_args()

results = []

for n in [50,100,200,400]:
    G = random_lift(5,n,4)
    r = cycle_rank(G)
    results.append({"n":n,"cycle_rank":int(r)})

with open(args.out,"w") as f:
    for row in results:
        f.write(json.dumps(row)+"\n")

print("done")
