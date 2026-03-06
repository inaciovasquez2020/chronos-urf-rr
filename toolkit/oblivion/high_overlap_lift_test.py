import networkx as nx
import random
import json

def random_lift(base_graph, n_lift):
    B = base_graph
    lifted = nx.Graph()
    for v in B.nodes():
        for i in range(n_lift):
            lifted.add_node((v,i))
    for (u,v) in B.edges():
        perm = list(range(n_lift))
        random.shuffle(perm)
        for i in range(n_lift):
            lifted.add_edge((u,i),(v,perm[i]))
    return lifted

def cycle_overlap_rank(G,R):
    edge_index={e:i for i,e in enumerate(G.edges())}
    basis=[]
    rank=0
    for v in G.nodes():
        B=nx.ego_graph(G,v,radius=R)
        for cyc in nx.cycle_basis(B):
            vec=[0]*len(edge_index)
            for i in range(len(cyc)):
                a=cyc[i]
                b=cyc[(i+1)%len(cyc)]
                e=tuple(sorted((a,b)))
                if e in edge_index:
                    vec[edge_index[e]]^=1
            x=vec[:]
            for p,bv in basis:
                if x[p]:
                    for j in range(len(x)):
                        x[j]^=bv[j]
            if any(x):
                pivot=x.index(1)
                basis.append((pivot,x))
                rank+=1
    return rank

def fo_types(G,r):
    import networkx.algorithms.graph_hashing as gh
    types=set()
    for v in G.nodes():
        B=nx.ego_graph(G,v,radius=r)
        types.add(gh.weisfeiler_lehman_graph_hash(B))
    return len(types)

def run():
    base=nx.complete_graph(4)
    lift=random_lift(base,40)
    C=cycle_overlap_rank(lift,2)
    T=fo_types(lift,2)
    return {
        "nodes":len(lift.nodes()),
        "edges":len(lift.edges()),
        "cycle_rank":C,
        "fo_types":T
    }

results=[run() for _ in range(10)]
print(json.dumps(results,indent=2))
