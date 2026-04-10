import json
from collections import deque

R = 2

def heawood():
    return {
        0:[1,5,13],1:[0,2,10],2:[1,3,7],3:[2,4,12],
        4:[3,5,9],5:[0,4,6],6:[5,7,11],7:[2,6,8],
        8:[7,9,13],9:[4,8,10],10:[1,9,11],11:[6,10,12],
        12:[3,11,13],13:[0,8,12],
    }

def disjoint_union(k):
    base = heawood()
    adj = {}
    offset = 0
    for _ in range(k):
        for u in base:
            adj[u+offset] = [v+offset for v in base[u]]
        offset += len(base)
    return adj

def edge_list(adj):
    return [(u,v) for u in adj for v in adj[u] if u<v]

def pack_edges(adj):
    chosen = []
    for e in edge_list(adj):
        if all(e[0] not in f and e[1] not in f for f in chosen):
            chosen.append(e)
    return chosen

def generate_lift(adj, twists):
    lift = {(u,b):set() for u in adj for b in (0,1)}
    for u,v in edge_list(adj):
        sigma = 1 if (u,v) in twists or (v,u) in twists else 0
        for b in (0,1):
            x=(u,b); y=(v,b^sigma)
            lift[x].add(y); lift[y].add(x)
    return {k:sorted(v) for k,v in lift.items()}

def compute_gap(k):
    B = disjoint_union(k)
    M = pack_edges(B)
    return len(M)

def main():
    results = []
    for k in [2,4,6,8]:
        gap = compute_gap(k)
        results.append({"blocks":k,"gap":gap})
    with open("artifacts/heawood_family_gap.json","w") as f:
        json.dump(results,f,indent=2)

if __name__ == "__main__":
    main()
