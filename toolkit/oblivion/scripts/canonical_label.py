#!/usr/bin/env python3

from collections import deque

def canonical_ball_code_iso(G, root, R):
    ball = {root}
    q = deque([(root,0)])
    while q:
        x,d = q.popleft()
        if d==R: continue
        for y in G[x]:
            if y not in ball:
                ball.add(y)
                q.append((y,d+1))

    dist = {root:0}
    q = deque([root])
    while q:
        x = q.popleft()
        for y in G[x]:
            if y in ball and y not in dist:
                dist[y] = dist[x]+1
                q.append(y)

    nodes = sorted(ball)
    best = None

    # normalize by all root-preserving BFS labelings
    for start in [root]:
        order = [root]
        layers = {}
        for v in nodes:
            layers.setdefault(dist[v], []).append(v)

        for d in sorted(layers.keys()):
            if d == 0:
                continue
            layer = sorted(layers[d])
            order.extend(layer)

        idx = {v:i for i,v in enumerate(order)}

        edges = []
        for u in order:
            for v in G[u]:
                if v in ball and idx[u] < idx[v]:
                    edges.append((idx[u], idx[v]))

        rep = (tuple(sorted(edges)), tuple(dist[v] for v in order))
        if best is None or rep < best:
            best = rep

    return hash(best)
