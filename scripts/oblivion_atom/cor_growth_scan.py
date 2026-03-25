import networkx as nx
import random

def random_lift(base_graph,n):
    lift=nx.Graph()
    for v in base_graph.nodes():
        for i in range(n):
            lift.add_node((v,i))
    for u,v in base_graph.edges():
        perm=list(range(n))
        random.shuffle(perm)
        for i in range(n):
            lift.add_edge((u,i),(v,perm[i]))
    return lift

def cor_proxy(G,R):
    seen=set()
    for v in G.nodes():
        B=nx.ego_graph(G,v,radius=R)
        for cyc in nx.cycle_basis(B):
            seen.add(tuple(sorted(cyc)))
    return len(seen)

if __name__=="__main__":
    base=nx.cycle_graph(6)
    for n in [20,40,80,160,320]:
        G=random_lift(base,n)
        print(n,cor_proxy(G,2))
