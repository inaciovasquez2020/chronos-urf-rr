import argparse, json
import networkx as nx

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True)
args = parser.parse_args()

sizes=[50,100,200,400]

rows=[]
for n in sizes:
    G=nx.random_regular_graph(4,n)
    m=G.number_of_edges()
    rows.append({"n":n,"edges":m})

with open(args.out,"w") as f:
    for r in rows:
        f.write(json.dumps(r)+"\n")

print("done")
