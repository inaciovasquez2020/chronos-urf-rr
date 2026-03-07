#!/usr/bin/env python3
import random
import networkx as nx
import numpy as np

def random_graph(n, d):
    return nx.random_regular_graph(d, n)

def sample_cycles(G, max_len=8, limit=200):
    cycles = []
    for c in nx.cycle_basis(G):
        if len(c) <= max_len:
            edges = []
            for i in range(len(c)):
                u = c[i]
                v = c[(i+1)%len(c)]
                if u < v:
                    edges.append((u,v))
                else:
                    edges.append((v,u))
            cycles.append(tuple(sorted(edges)))
        if len(cycles) >= limit:
            break
    return cycles

def build_matrix(cycles):
    edges = sorted({e for C in cycles for e in C})
    edge_index = {e:i for i,e in enumerate(edges)}
    B = np.zeros((len(edges), len(cycles)), dtype=np.uint8)
    for j,C in enumerate(cycles):
        for e in C:
            B[edge_index[e], j] = 1
    return B

def rank_mod2(A):
    A = A.copy()
    r = 0
    m,n = A.shape
    for c in range(n):
        pivot = None
        for i in range(r,m):
            if A[i,c]:
                pivot = i
                break
        if pivot is None:
            continue
        A[[r,pivot]] = A[[pivot,r]]
        for i in range(m):
            if i != r and A[i,c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return r

def experiment(n=200, d=4):
    G = random_graph(n,d)
    cycles = sample_cycles(G)
    B = build_matrix(cycles)
    r = rank_mod2(B)
    m = B.shape[1]
    return m, r

if __name__ == "__main__":
    m,r = experiment()
    print("cycles:", m)
    print("rank:", r)
    if m>0:
        print("rank/m:", r/m)
