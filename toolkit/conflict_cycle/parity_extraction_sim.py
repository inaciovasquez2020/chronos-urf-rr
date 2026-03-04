import itertools
import random
import networkx as nx
import numpy as np

def gf2_rank(vectors):
    if len(vectors) == 0:
        return 0
    M = np.array(vectors, dtype=int) % 2
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if M[i, c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        M[[r, pivot]] = M[[pivot, r]]
        for i in range(rows):
            if i != r and M[i, c] == 1:
                M[i] ^= M[r]
        r += 1
        if r == rows:
            break
    return r

def random_regular_connected(n, d):
    while True:
        G = nx.random_regular_graph(d, n)
        if nx.is_connected(G):
            return G

def edge_index(G):
    edges = list(G.edges())
    idx = {}
    for i,(u,v) in enumerate(edges):
        if u>v:
            u,v=v,u
        idx[(u,v)] = i
    return edges, idx

def random_clause(m):
    size = random.randint(1,6)
    vars = random.sample(range(m), size)
    clause = []
    for v in vars:
        lit = v+1
        if random.random() < 0.5:
            lit = -lit
        clause.append(lit)
    return tuple(sorted(set(clause), key=lambda x:(abs(x),x)))

def clause_vector(clause, m):
    v = np.zeros(m,dtype=int)
    for lit in clause:
        v[abs(lit)-1] ^= 1
    return v

def simulate(n=80,d=3,steps=20000):
    G = random_regular_connected(n,d)
    edges,idx = edge_index(G)
    m=len(edges)

    clauses=set()
    vectors=[]

    for _ in range(50):
        c=random_clause(m)
        clauses.add(c)
        vectors.append(clause_vector(c,m))

    max_rank=gf2_rank(vectors)

    for t in range(steps):

        c1,c2=random.sample(list(clauses),2)

        common=set(abs(x) for x in c1).intersection(set(abs(x) for x in c2))
        if not common:
            continue

        pivot=random.choice(list(common))

        r=set(c1).union(set(c2))
        r.discard(pivot)
        r.discard(-pivot)

        if any(-x in r for x in r):
            continue

        r=tuple(sorted(r,key=lambda x:(abs(x),x)))

        if r not in clauses:
            clauses.add(r)
            v=clause_vector(r,m)
            vectors.append(v)
            rank=gf2_rank(vectors)
            max_rank=max(max_rank,rank)

    print("nodes",n)
    print("edges",m)
    print("max_parity_rank",max_rank)

if __name__=="__main__":
    simulate()
