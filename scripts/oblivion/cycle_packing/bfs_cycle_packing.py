# scripts/oblivion/cycle_packing/bfs_cycle_packing.py

import networkx as nx
import collections

def bfs_cycle(G,start,L):

    visited={start:None}
    depth={start:0}
    q=collections.deque([start])

    while q:
        v=q.popleft()

        if depth[v] >= L:
            continue

        for u in G[v]:

            if u not in visited:
                visited[u]=v
                depth[u]=depth[v]+1
                q.append(u)

            elif visited[v] != u:
                cycle=[v]
                x=v

                while x!=u and x is not None:
                    x=visited[x]
                    cycle.append(x)

                return cycle

    return None

def cycle_packing(G,L):

    H=G.copy()
    cycles=[]

    for v in list(H.nodes()):
        c=bfs_cycle(H,v,L)

        if c:
            cycles.append(c)

            edges=[(c[i],c[i+1]) for i in range(len(c)-1)]

            H.remove_edges_from(edges)

    return cycles
