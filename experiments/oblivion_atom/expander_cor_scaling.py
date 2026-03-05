import networkx as nx

def cor_proxy(G,R):
    seen=set()
    for v in G.nodes():
        B=nx.ego_graph(G,v,radius=R)
        for cyc in nx.cycle_basis(B):
            seen.add(tuple(sorted(cyc)))
    return len(seen)

for n in [100,200,400,800]:
    G=nx.random_regular_graph(4,n)
    print(n,cor_proxy(G,2))
