# toolkit/oblivion/scripts/ef_configuration_repeat_test.py

import networkx as nx
from collections import deque, defaultdict
import json
import argparse


def r_ball(G, v, R):
    nodes = nx.single_source_shortest_path_length(G, v, cutoff=R).keys()
    return G.subgraph(nodes).copy()


def ball_signature(G, v, R):
    B = r_ball(G, v, R)
    return (B.number_of_nodes(), B.number_of_edges())


def config_signature(G, H, a, b, R):
    sig_g = tuple(ball_signature(G, x, R) for x in a)
    sig_h = tuple(ball_signature(H, x, R) for x in b)
    return (sig_g, sig_h)


def neighbors(G, v):
    return list(G.neighbors(v))


def generate_moves(G, H, a, b):
    moves = []
    for i in range(len(a)):
        for u in neighbors(G, a[i]):
            new_a = list(a)
            new_a[i] = u
            for w in neighbors(H, b[i]):
                new_b = list(b)
                new_b[i] = w
                moves.append((tuple(new_a), tuple(new_b)))
    return moves


def explore(G, H, k, R, depth_limit=200):
    start_a = tuple(list(G.nodes())[:k])
    start_b = tuple(list(H.nodes())[:k])

    visited = set()
    config_seen = defaultdict(int)

    queue = deque()
    queue.append((start_a, start_b, 0))

    while queue:
        a, b, d = queue.popleft()
        if d > depth_limit:
            break

        state = (a, b)
        if state in visited:
            continue
        visited.add(state)

        cfg = config_signature(G, H, a, b, R)
        config_seen[cfg] += 1

        for na, nb in generate_moves(G, H, a, b):
            queue.append((na, nb, d + 1))

    return {
        "states_explored": len(visited),
        "distinct_configurations": len(config_seen),
        "max_repeat_count": max(config_seen.values()) if config_seen else 0,
    }


def build_cycle(n):
    return nx.cycle_graph(n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--R", type=int, default=2)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    G = build_cycle(args.n)
    H = build_cycle(args.n + 2)

    result = explore(G, H, args.k, args.R)

    with open(args.out, "w") as f:
        f.write(json.dumps(result) + "\n")

    print(result)


if __name__ == "__main__":
    main()
