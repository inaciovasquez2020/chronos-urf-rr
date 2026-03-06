import networkx as nx

def cor_estimate(G,R):
    count=0
    for v in G.nodes():
        B=nx.ego_graph(G,v,radius=R)
        count+=len(nx.cycle_basis(B))
    return count

if __name__=="__main__":
    G=nx.random_regular_graph(4,200)
    print("COR estimate:",cor_estimate(G,2))
