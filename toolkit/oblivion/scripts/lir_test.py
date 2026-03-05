import argparse
import networkx as nx
import numpy as np


def ladder_graph(n):
    return nx.ladder_graph(n)


def torus_graph(n):
    return nx.grid_2d_graph(n, n, periodic=True)


def random_regular_graph(n, d=3):
    return nx.random_regular_graph(d, n)


def cycle_graph(n):
    return nx.cycle_graph(n)


def cycle_of_cycles(n):
    G = nx.Graph()
    for i in range(n):
        a = (i, "a")
        b = (i, "b")
        c = (i, "c")
        d = (i, "d")

        G.add_edges_from([(a, b), (b, c), (c, d), (d, a)])

        if i > 0:
            G.add_edge((i - 1, "c"), a)

    return G


def triangular_grid(n):
    G = nx.Graph()
    for i in range(n):
        for j in range(n):
            v = (i, j)
            G.add_edge(v, ((i + 1) % n, j))
            G.add_edge(v, (i, (j + 1) % n))
            G.add_edge(v, ((i + 1) % n, (j + 1) % n))
    return G


def ball(G, v, R):
    nodes = nx.single_source_shortest_path_length(G, v, R).keys()
    return G.subgraph(nodes).copy()


def cycle_basis_edges(G):
    cycles = nx.cycle_basis(G)
    edge_sets = []

    for c in cycles:
        edges = set()
        for i in range(len(c)):
            a = c[i]
            b = c[(i + 1) % len(c)]
            edges.add(tuple(sorted((a, b))))
        edge_sets.append(edges)

    return edge_sets


def interaction_rank(cycles):
    m = len(cycles)
    if m == 0:
        return 0

    M = np.zeros((m, m), dtype=int)

    for i in range(m):
        for j in range(m):
            if cycles[i].intersection(cycles[j]):
                M[i, j] = 1

    return np.linalg.matrix_rank(M % 2)


def LIR(G, R):
    max_rank = 0

    for v in G.nodes():
        B = ball(G, v, R)
        cycles = cycle_basis_edges(B)
        r = interaction_rank(cycles)

        if r > max_rank:
            max_rank = r

    return max_rank


def scan_radius(G, maxR):
    for r in range(1, maxR + 1):
        val = LIR(G, r)
        print("R =", r, "LIR =", val)


parser = argparse.ArgumentParser()

parser.add_argument(
    "--graph",
    choices=["ladder", "torus", "random", "cycle", "cyclechain", "triangular"],
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
    scan_radius(G, args.R)
else:
    print("nodes:", len(G))
    print("edges:", len(G.edges()))
    print("LIR_R(G) =", LIR(G, args.R))
