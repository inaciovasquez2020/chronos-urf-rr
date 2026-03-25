import networkx as nx
import itertools
import json
from collections import defaultdict

def local_cycles(G, v, R):
    B = nx.ego_graph(G, v, radius=R)
    cycles = nx.cycle_basis(B)
    edgesets = []
    for c in cycles:
        edges = set()
        for i in range(len(c)):
            a = c[i]
            b = c[(i+1)%len(c)]
            edges.add(tuple(sorted((a,b))))
        edgesets.append(edges)
    return edgesets

def cycle_overlap_rank(G, R):
    edge_index = {e:i for i,e in enumerate(G.edges())}
    vectors = []
    for v in G.nodes():
        for cyc in local_cycles(G,v,R):
            vec = [0]*len(edge_index)
            for e in cyc:
                if e in edge_index:
                    vec[edge_index[e]] ^= 1
            vectors.append(vec)
    rank = 0
    basis = []
    for v in vectors:
        x = v[:]
        for b in basis:
            if x[b[0]]:
                for i in range(len(x)):
                    x[i] ^= b[1][i]
        if any(x):
            pivot = x.index(1)
            basis.append((pivot,x))
            rank += 1
    return rank

def fo_type(G,v,r):
    B = nx.ego_graph(G,v,radius=r)
    return nx.weisfeiler_lehman_graph_hash(B)

def fo_type_diversity(G,r):
    types = set()
    for v in G.nodes():
        types.add(fo_type(G,v,r))
    return len(types)

def run(n=200,deg=3,R=2,r=2):
    G = nx.random_regular_graph(deg,n)
    C = cycle_overlap_rank(G,R)
    T = fo_type_diversity(G,r)
    return {"n":n,"deg":deg,"cycle_rank":C,"fo_types":T}

if __name__=="__main__":
    results=[]
    for i in range(10):
        results.append(run())
    print(json.dumps(results,indent=2))
