#!/usr/bin/env python3

from .rooted_wl import wl_refinement
from .clr_local_transition_scan import cycle_rank

def local_cycle_rank(G, v, R):
    ball = {v}
    frontier = [(v,0)]
    while frontier:
        x,d = frontier.pop()
        if d==R: continue
        for y in G[x]:
            if y not in ball:
                ball.add(y)
                frontier.append((y,d+1))

    edges = 0
    for u in ball:
        for w in G[u]:
            if w in ball:
                edges += 1
    edges //= 2

    return edges - len(ball) + 1

def I(G, R):
    counts = {}
    for v in G:
        t = wl_refinement(G, v, R)
        counts.setdefault(t, []).append(v)

    total = 0
    for tau, verts in counts.items():
        beta = sum(local_cycle_rank(G, v, R) for v in verts) / len(verts)
        total += len(verts) * (beta ** 2)

    return total

def small_twist_pair():
    # minimal nontrivial difference: add one cycle
    G0 = {
        0:{1},1:{0,2},2:{1}
    }
    G1 = {
        0:{1,2},1:{0,2},2:{0,1}  # triangle
    }
    return G0, G1

def run():
    R = 2
    G0, G1 = small_twist_pair()

    print("I(G0) =", I(G0,R))
    print("I(G1) =", I(G1,R))
    print("cycle ranks:", cycle_rank(G0), cycle_rank(G1))

if __name__ == "__main__":
    run()
