# toolkit/oblivion/scripts/lcake_compute.py

import networkx as nx
import argparse
import json

def ball_subgraph(G, v, R):
    nodes = nx.single_source_shortest_path_length(G, v, cutoff=R).keys()
    return G.subgraph(nodes).copy()

def cycle_space_basis(G):
    return nx.cycle_basis(G)

def edge_index(G):
    edges = list(G.edges())
    idx = {}
    for i,(u,v) in enumerate(edges):
        idx[(u,v)] = i
        idx[(v,u)] = i
    return idx, len(edges)

def cycle_vector(cycle, edge_map, m):
    vec = [0]*m
    for i in range(len(cycle)):
        u = cycle[i]
        v = cycle[(i+1)%len(cycle)]
        vec[edge_map[(u,v)]] ^= 1
    return vec

def gf2_rank(vectors):
    basis = []
    for v in vectors:
        v = v[:]
        for b in basis:
            pivot = next((i for i,x in enumerate(b) if x), None)
            if pivot is not None and v[pivot]:
                for j in range(len(v)):
                    v[j] ^= b[j]
        if any(v):
            pivot = next(i for i,x in enumerate(v) if x)
            basis.append(v)
    return len(basis)

def compute_lcake(G,R):
    edge_map,m = edge_index(G)
    vectors = []

    for v in G.nodes():
        B = ball_subgraph(G,v,R)
        cycles = cycle_space_basis(B)
        for c in cycles:
            vectors.append(cycle_vector(c,edge_map,m))

    return gf2_rank(vectors)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n",type=int,default=50)
    parser.add_argument("--d",type=int,default=3)
    parser.add_argument("--R",type=int,default=2)
    parser.add_argument("--out",type=str,default="lcake_result.json")
    args = parser.parse_args()

    G = nx.random_regular_graph(args.d,args.n)

    val = compute_lcake(G,args.R)

    result = {
        "n":args.n,
        "degree":args.d,
        "R":args.R,
        "lcake":val
    }

    with open(args.out,"w") as f:
        json.dump(result,f,indent=2)

if __name__=="__main__":
    main()
