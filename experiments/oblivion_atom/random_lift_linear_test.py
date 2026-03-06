import networkx as nx
import random

def random_lift(base,n):
    G=nx.Graph()
    for v in base.nodes():
        for i in range(n):
            G.add_node((v,i))
    for u,v in base.edges():
        perm=list(range(n))
        random.shuffle(perm)
        for i in range(n):
            G.add_edge((u,i),(v,perm[i]))
    return G

def cor_proxy(G,R):
    seen=set()
    for v in G.nodes():
        B=nx.ego_graph(G,v,radius=R)
        for cyc in nx.cycle_basis(B):
            seen.add(tuple(sorted(cyc)))
    return len(seen)

base=nx.cycle_graph(5)

for n in [20,40,80,160]:
    G=random_lift(base,n)
    print("n =",n,"COR proxy =",cor_proxy(G,2))
