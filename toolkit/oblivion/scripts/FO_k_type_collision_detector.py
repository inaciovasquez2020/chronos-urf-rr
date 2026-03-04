import argparse, json
import networkx as nx

def local_signature(G,v,r=2):
    nodes=nx.single_source_shortest_path_length(G,v,r).keys()
    H=G.subgraph(nodes)
    return (H.number_of_nodes(),H.number_of_edges())

parser=argparse.ArgumentParser()
parser.add_argument("--out",required=True)
args=parser.parse_args()

rows=[]
for n in [50,100,200]:
    G=nx.random_regular_graph(4,n)
    sigs=set()
    for v in G.nodes():
        sigs.add(local_signature(G,v))
    rows.append({"n":n,"distinct_types":len(sigs)})

with open(args.out,"w") as f:
    for r in rows:
        f.write(json.dumps(r)+"\n")

print("done")
