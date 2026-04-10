import json
from collections import deque

R = 2

def heawood():
    adj = {
        0: [1, 5, 13],
        1: [0, 2, 10],
        2: [1, 3, 7],
        3: [2, 4, 12],
        4: [3, 5, 9],
        5: [0, 4, 6],
        6: [5, 7, 11],
        7: [2, 6, 8],
        8: [7, 9, 13],
        9: [4, 8, 10],
        10: [1, 9, 11],
        11: [6, 10, 12],
        12: [3, 11, 13],
        13: [0, 8, 12],
    }
    return {k: sorted(v) for k,v in adj.items()}

def disjoint_union(graphs):
    adj = {}
    offset = 0
    for g in graphs:
        n = len(g)
        for u in g:
            adj[u+offset] = [v+offset for v in g[u]]
        offset += n
    return adj

def edge_list(adj):
    out = []
    for u in adj:
        for v in adj[u]:
            if u < v:
                out.append((u,v))
    return out

def generate_lift(base, twisted_edges):
    lift = {(u,b):set() for u in base for b in (0,1)}
    for u,v in edge_list(base):
        sigma = 1 if (u,v) in twisted_edges or (v,u) in twisted_edges else 0
        for b in (0,1):
            x=(u,b); y=(v,b^sigma)
            lift[x].add(y); lift[y].add(x)
    return {k:sorted(v) for k,v in lift.items()}

def pack_edges(base):
    chosen = []
    for e in edge_list(base):
        ok = True
        for f in chosen:
            if e[0]==f[0] or e[0]==f[1] or e[1]==f[0] or e[1]==f[1]:
                ok=False
        if ok:
            chosen.append(e)
    return chosen

def main():
    k = 8
    base_blocks = [heawood() for _ in range(k)]
    Bn = disjoint_union(base_blocks)

    M = pack_edges(Bn)

    Gp = generate_lift(Bn, twisted_edges=[])
    Gm = generate_lift(Bn, twisted_edges=M)

    out = {
        "blocks": k,
        "num_vertices_base": len(Bn),
        "num_twists": len(M),
        "twisted_edges": M[:10],
        "expected_gap_lower_bound": len(M),
    }

    with open("artifacts/heawood_family_summary.json","w") as f:
        json.dump(out,f,indent=2)

if __name__ == "__main__":
    main()
