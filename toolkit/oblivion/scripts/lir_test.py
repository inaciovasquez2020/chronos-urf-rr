import argparse
import random
import networkx as nx
from itertools import combinations

def cycle_graph(n):
    return nx.cycle_graph(n)

def ladder_graph(n):
    return nx.ladder_graph(n)

def torus_graph(n):
    return nx.grid_2d_graph(n, n, periodic=True)

def triangular_grid(n):
    G = nx.Graph()
    for i in range(n):
        for j in range(n):
            v = (i, j)
            G.add_node(v)
            for di, dj in [(1,0),(0,1),(1,1)]:
                u = ((i+di)%n,(j+dj)%n)
                G.add_edge(v,u)
    return G

def random_regular_graph(n, d=3):
    return nx.random_regular_graph(d, n)

def cycle_of_cycles(k):
    G = nx.Graph()
    offset = 0
    cycles = []
    for _ in range(k):
        C = nx.cycle_graph(6)
        mapping = {v:v+offset for v in C.nodes()}
        C = nx.relabel_nodes(C, mapping)
        G = nx.compose(G, C)
        cycles.append([v+offset for v in range(6)])
        offset += 6
    for i in range(k):
        G.add_edge(cycles[i][0], cycles[(i+1)%k][3])
    return G

def radius_ball(G, v, R):
    nodes = nx.single_source_shortest_path_length(G, v, cutoff=R).keys()
    return G.subgraph(nodes)

def cycle_basis_edges(G):
    cycles = nx.cycle_basis(G)
    edge_sets = []
    for c in cycles:
        edges = set()
        for i in range(len(c)):
            u = c[i]
            v = c[(i+1)%len(c)]
            edges.add(tuple(sorted((u,v))))
        edge_sets.append(edges)
    return edge_sets

def overlap_graph(cycles):
    H = nx.Graph()
    for i in range(len(cycles)):
        H.add_node(i)
    for i,j in combinations(range(len(cycles)),2):
        if cycles[i] & cycles[j]:
            H.add_edge(i,j)
    return H

def LIR(G,R):
    max_lir = 0
    for v in G.nodes():
        B = radius_ball(G,v,R)
        cycles = cycle_basis_edges(B)
        H = overlap_graph(cycles)
        for comp in nx.connected_components(H):
            max_lir = max(max_lir,len(comp))
    return max_lir

def scan_radius(G,maxR):
    for r in range(1,maxR+1):
        print("R =",r,"LIR =",LIR(G,r))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--graph",
        choices=["ladder","torus","random","cycle","cyclechain","triangular"],
    )

    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--R", type=int, default=2)
    parser.add_argument("--scan", action="store_true")

    args = parser.parse_args()

    if args.graph == "ladder":
        G = ladder_graph(args.n)
    elif args.graph == "torus":
        G = torus_graph(args.n)
    elif args.graph == "random":
        G = random_regular_graph(args.n)
    elif args.graph == "cycle":
        G = cycle_graph(args.n)
    elif args.graph == "cyclechain":
        G = cycle_of_cycles(args.n)
    else:
        G = triangular_grid(args.n)

    if args.scan:
        scan_radius(G,args.R)
    else:
        print("nodes:",len(G))
        print("edges:",len(G.edges()))
        print("LIR_R(G) =",LIR(G,args.R))

if __name__ == "__main__":
    main()
