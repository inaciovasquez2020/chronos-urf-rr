#!/usr/bin/env python3
import json, argparse, collections

def load_graph(path):
    data = json.load(open(path))
    adj = data["adj"]
    return adj

def ball_size(adj, start, R):
    seen = {start}
    frontier = {start}
    for _ in range(R):
        nxt = set()
        for v in frontier:
            for u in adj[v]:
                if u not in seen:
                    seen.add(u)
                    nxt.add(u)
        frontier = nxt
    return len(seen)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph_json", required=True)
    ap.add_argument("--max_R", type=int, default=6)
    args = ap.parse_args()

    adj = load_graph(args.graph_json)

    for r in range(1, args.max_R+1):
        print(r, ball_size(adj, 0, r))

if __name__ == "__main__":
    main()
