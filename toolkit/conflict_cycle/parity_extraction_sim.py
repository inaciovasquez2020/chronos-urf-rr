import random
import itertools

def random_regular_connected(n, d):
    while True:
        stubs = []
        for v in range(n):
            stubs += [v]*d
        random.shuffle(stubs)

        edges = set()
        ok = True

        for i in range(0, len(stubs), 2):
            u = stubs[i]
            v = stubs[i+1]
            if u == v:
                ok = False
                break
            e = tuple(sorted((u, v)))
            if e in edges:
                ok = False
                break
            edges.add(e)

        if not ok:
            continue

        adj = {i: set() for i in range(n)}
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)

        seen = set()
        stack = [0]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(adj[x] - seen)

        if len(seen) == n:
            return list(edges)

def gf2_rank(vectors):
    basis = []
    for v in vectors:
        x = v
        for b in basis:
            if x == 0:
                break
            x = min(x, x ^ b)
        if x:
            basis.append(x)
    return len(basis)

def cut_vector(U, edge_index):
    vec = 0
    for (u, v), idx in edge_index.items():
        if (u in U) ^ (v in U):
            vec ^= (1 << idx)
    return vec

def simulate(n=160, d=3, steps=100000):
    edges = random_regular_connected(n, d)
    m = len(edges)

    edge_index = {e:i for i,e in enumerate(edges)}

    clauses = []
    max_rank = 0

    for t in range(1, steps+1):
        size = random.randint(1, n//2)
        U = set(random.sample(range(n), size))

        vec = cut_vector(U, edge_index)
        clauses.append(vec)

        rank = gf2_rank(clauses)

        if rank > max_rank:
            max_rank = rank

        if t % 15000 == 0:
            print("t", t, "clauses", len(clauses), "rank", rank, "max_rank", max_rank)

    print()
    print("FINAL RESULT")
    print("nodes", n)
    print("edges", m)
    print("clauses_final", len(clauses))
    print("max_parity_rank", max_rank)

if __name__ == "__main__":
    simulate(n=160, d=4, steps=100000)
