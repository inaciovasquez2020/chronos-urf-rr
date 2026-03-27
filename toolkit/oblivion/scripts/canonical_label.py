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

    nodes = sorted(ball)
    best = None

    for start in nodes:
        dist = {start:0}
        q = deque([start])
        while q:
            x = q.popleft()
            for y in G[x]:
                if y in ball and y not in dist:
                    dist[y] = dist[x]+1
                    q.append(y)

        order = sorted(ball, key=lambda v:(dist.get(v,999), len(G[v]), v))
        idx = {v:i for i,v in enumerate(order)}

        edges = []
        for u in order:
            for v in G[u]:
                if v in ball and idx[u] < idx[v]:
                    edges.append((idx[u], idx[v]))

        rep = (tuple(sorted(edges)), tuple(sorted(dist.values())))
        if best is None or rep < best:
            best = rep

    return hash(best)
