#!/usr/bin/env python3

def wl_refinement(G, root, R, iters=3):
    # extract ball
    ball = {root}
    frontier = [(root,0)]
    while frontier:
        x,d = frontier.pop()
        if d==R: continue
        for y in G[x]:
            if y not in ball:
                ball.add(y)
                frontier.append((y,d+1))

    # initial colors: distance + degree
    dist = {root:0}
    frontier = [root]
    while frontier:
        x = frontier.pop()
        for y in G[x]:
            if y in ball and y not in dist:
                dist[y] = dist[x]+1
                frontier.append(y)

    color = {v:(dist[v], len(G[v])) for v in ball}

    for _ in range(iters):
        new_color = {}
        for v in ball:
            neigh = sorted(color[u] for u in G[v] if u in ball)
            new_color[v] = (color[v], tuple(neigh))
        # relabel to compact ints
        mapping = {c:i for i,c in enumerate(sorted(set(new_color.values())))}
        color = {v:mapping[new_color[v]] for v in ball}

    return tuple(sorted(color.values()))

def count_types_wl(G, R):
    reps = []
    sigs = []
    for v in G:
        sig = wl_refinement(G, v, R)
        if sig not in sigs:
            sigs.append(sig)
            reps.append(v)
    return len(reps)
