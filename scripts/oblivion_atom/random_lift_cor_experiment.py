import networkx as nx
import random

def random_lift(base_graph, n):
    lift = nx.Graph()
    for v in base_graph.nodes():
        for i in range(n):
            lift.add_node((v,i))
    for u,v in base_graph.edges():
        perm=list(range(n))
        random.shuffle(perm)
        for i in range(n):
            lift.add_edge((u,i),(v,perm[i]))
    return lift

def radius_ball(G,v,R):
    nodes={v}
    frontier={v}
    for _ in range(R):
        new=set()
        for x in frontier:
            new.update(G.neighbors(x))
        frontier=new-nodes
        nodes|=frontier
    return G.subgraph(nodes)

def count_local_cycles(G,R):
    cycles=set()
    for v in G.nodes():
        B=radius_ball(G,v,R)
        for C in nx.cycle_basis(B):
            cycles.add(tuple(sorted(C)))
    return len(cycles)

if __name__=="__main__":
    base=nx.cycle_graph(4)
    for n in [10,20,40]:
        G=random_lift(base,n)
        c=count_local_cycles(G,2)
        print("n",n,"local cycles",c)
