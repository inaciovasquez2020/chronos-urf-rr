import networkx as nx
import numpy as np
import random

# ---------- helpers ----------

def cycle_edge_matrix(cycles):
    edges = sorted({tuple(sorted(e)) for C in cycles for e in C})
    idx = {e:i for i,e in enumerate(edges)}
    M = np.zeros((len(edges), len(cycles)), dtype=np.uint8)
    for j,C in enumerate(cycles):
        for e in C:
            M[idx[tuple(sorted(e))], j] = 1
    return M

def rank_mod2(A):
    A=A.copy()
    r=0
    m,n=A.shape
    for c in range(n):
        pivot=None
        for i in range(r,m):
            if A[i,c]:
                pivot=i; break
        if pivot is None: continue
        A[[r,pivot]]=A[[pivot,r]]
        for i in range(m):
            if i!=r and A[i,c]:
                A[i]^=A[r]
        r+=1
        if r==m: break
    return r

def row_signatures(M):
    return len({tuple(row) for row in M})

# ---------- adversarial constructions ----------

def ladder_graph(n):
    G=nx.Graph()
    for i in range(n):
        G.add_edge(("a",i),("a",i+1))
        G.add_edge(("b",i),("b",i+1))
        G.add_edge(("a",i),("b",i))
    return G

def torus_grid(n):
    G=nx.grid_2d_graph(n,n,periodic=True)
    return nx.convert_node_labels_to_integers(G)

def overlapping_cycles(base, repeats):
    cycles=[]
    for i in range(repeats):
        C=[(base[j],base[j+1]) for j in range(len(base)-1)]
        C.append((base[-1],base[0]))
        cycles.append(C)
    return cycles

def cycle_basis_edges(G):
    cycles=[]
    for C in nx.cycle_basis(G):
        edges=[]
        for i in range(len(C)):
            u=C[i]; v=C[(i+1)%len(C)]
            edges.append((u,v))
        cycles.append(edges)
    return cycles

# ---------- tests ----------

def test_graph(G,name):
    cycles=cycle_basis_edges(G)
    if not cycles: 
        return
    M=cycle_edge_matrix(cycles)
    r=rank_mod2(M)
    sig=row_signatures(M.T)
    m=len(cycles)
    print(name)
    print("cycles:",m)
    print("rank:",r)
    print("rank/m:", r/m if m else 0)
    print("unique signatures:",sig)
    print()

# ---------- run ----------

random.seed(0)

# ladder
G=ladder_graph(20)
test_graph(G,"ladder")

# torus grid
G=torus_grid(8)
test_graph(G,"torus grid")

# repeated cycle gadget
base=list(range(10))
cycles=overlapping_cycles(base,30)
M=cycle_edge_matrix(cycles)
print("repeated cycle gadget")
print("cycles:",len(cycles))
print("rank:",rank_mod2(M))
print("unique signatures:",row_signatures(M.T))
print()

print("done")
