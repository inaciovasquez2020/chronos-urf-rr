import networkx as nx
import random
from collections import defaultdict

def random_lift(base_graph, n, seed=0):
    rng = random.Random(seed)
    lift = nx.Graph()
    for v in base_graph.nodes():
        for i in range(n):
            lift.add_node((v,i))
    for u,v in base_graph.edges():
        perm=list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            lift.add_edge((u,i),(v,perm[i]))
    return lift

def ball(G, v, R):
    return nx.ego_graph(G, v, radius=R)

def local_cycle_basis_edges(G, R, limit_vertices=None):
    # returns a multiset proxy: counts of distinct cycle edge-sets appearing in some ball
    seen=set()
    it = G.nodes() if limit_vertices is None else limit_vertices
    for v in it:
        B = ball(G, v, R)
        for cyc in nx.cycle_basis(B):
            edges=[]
            for i in range(len(cyc)):
                a=cyc[i]
                b=cyc[(i+1)%len(cyc)]
                if a>b: a,b=b,a
                edges.append((a,b))
            edges=tuple(sorted(edges))
            seen.add(edges)
    return len(seen)

if __name__ == "__main__":
    base = nx.cycle_graph(6)
    R = 2
    for n in [20, 40, 80, 160]:
        G = random_lift(base, n, seed=7)
        proxy = local_cycle_basis_edges(G, R)
        print(f"n={n:4d} |V|={G.number_of_nodes():6d} proxy_unique_local_cycles={proxy}")
