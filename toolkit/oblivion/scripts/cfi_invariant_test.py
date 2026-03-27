#!/usr/bin/env python3

from cfi_pair_generator import cfi_pair_on_cycle
from rooted_wl import wl_refinement

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
    classes = {}
    for v in G:
        t = wl_refinement(G, v, R)
        classes.setdefault(t, []).append(v)

    total = 0
    for verts in classes.values():
        beta = sum(local_cycle_rank(G, v, R) for v in verts) / len(verts)
        total += len(verts) * (beta ** 2)

    return total

def run():
    R = 2
    G0, G1 = cfi_pair_on_cycle(6, {(0,1)})

    print("I(G0) =", I(G0,R))
    print("I(G1) =", I(G1,R))

if __name__ == "__main__":
    run()
