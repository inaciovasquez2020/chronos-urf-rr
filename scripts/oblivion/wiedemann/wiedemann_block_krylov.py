# scripts/oblivion/wiedemann/wiedemann_block_krylov.py

import numpy as np
from scipy.sparse import csr_matrix

def gf2_mv(A,v):
    return (A.dot(v) % 2).astype(np.uint8)

def block_krylov(A, block=16, steps=128):
    n=A.shape[0]
    V=np.random.randint(0,2,(n,block),dtype=np.uint8)
    K=[V]
    X=V

    for _ in range(steps):
        X=gf2_mv(A,X)
        K.append(X)

    return np.concatenate(K,axis=1)

def rank_estimate(A):
    K=block_krylov(A)
    return np.linalg.matrix_rank(K % 2)
