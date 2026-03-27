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

    # enforce root mapped to index 0
    for perm_root in [root]:
        order = sorted(nodes, key=lambda v:(dist[v], len(G[v]), v))
        if order[0] != root:
            order.remove(root)
            order = [root] + order

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
