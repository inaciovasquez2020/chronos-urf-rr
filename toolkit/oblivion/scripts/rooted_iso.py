#!/usr/bin/env python3

from itertools import permutations

def rooted_ball(G, root, R):
    ball = {root}
    frontier = [(root,0)]
    while frontier:
        x,d = frontier.pop()
        if d==R: continue
        for y in G[x]:
            if y not in ball:
                ball.add(y)
                frontier.append((y,d+1))
    return ball

def induced_edges(G, ball):
    edges = set()
    for u in ball:
        for v in G[u]:
            if v in ball and u < v:
                edges.add((u,v))
    return edges

def rooted_iso(G, u, v, R):
    Bu = rooted_ball(G,u,R)
    Bv = rooted_ball(G,v,R)

    if len(Bu) != len(Bv):
        return False

    nodes_u = list(Bu)
    nodes_v = list(Bv)

    edges_u = induced_edges(G,Bu)
    edges_v = induced_edges(G,Bv)

    for perm in permutations(nodes_v):
        mapping = dict(zip(nodes_u, perm))
        if mapping[u] != v:
            continue

        ok = True
        for a,b in edges_u:
            if (mapping[a], mapping[b]) not in edges_v and (mapping[b], mapping[a]) not in edges_v:
                ok = False
                break

        if ok:
            return True

    return False
