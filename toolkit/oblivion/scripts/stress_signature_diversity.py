import random
import numpy as np

def generate_matrix(V, m, B, L):
    M = np.zeros((V,m),dtype=int)

    vertex_usage = [0]*V

    for j in range(m):
        size = random.randint(1,B)
        vertices = []

        for _ in range(size):
            v = random.randrange(V)
            if vertex_usage[v] < L:
                vertices.append(v)
                vertex_usage[v]+=1

        for v in vertices:
            M[v,j]=1

    return M

def count_unique_rows(M):
    rows=set()
    for r in M:
        rows.add(tuple(r))
    return len(rows)

for _ in range(1000):

    V=50
    m=40
    B=4
    L=4

    M=generate_matrix(V,m,B,L)

    unique=count_unique_rows(M)

    if unique < m/(B*L):

        print("counterexample found")
        print("rows",unique)
        print("expected >=",m/(B*L))
        break
else:
    print("no counterexample found")
