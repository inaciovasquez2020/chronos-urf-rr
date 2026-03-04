# toolkit/conflict_cycle/parity_extraction_sim.py

import random
import numpy as np


def random_clause_vector(n):
    """
    Generate a random GF(2) vector representing a clause.
    """
    v = np.zeros(n, dtype=np.uint8)
    size = random.randint(1, min(5, n))
    idxs = random.sample(range(n), size)
    for i in idxs:
        v[i] ^= 1
    return v


def rank_mod2(matrix):
    """
    Compute rank of a binary matrix over GF(2) using Gaussian elimination.
    """
    if len(matrix) == 0:
        return 0

    M = np.array(matrix, dtype=np.uint8)
    rows, cols = M.shape
    r = 0

    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if M[i, c]:
                pivot = i
                break
        if pivot is None:
            continue

        M[[r, pivot]] = M[[pivot, r]]

        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]

        r += 1
        if r == rows:
            break

    return r


def run_simulation():
    n = 159
    clauses = []
    rank = 0
    max_rank = n

    t = 0

    while True:
        t += 1

        clause = random_clause_vector(n)
        clauses.append(clause)

        new_rank = rank_mod2(clauses)

        if new_rank > rank:
            rank = new_rank

        if t % 15000 == 0:
            print("t", t, "clauses", len(clauses), "rank", rank, "max_rank", max_rank)

        if rank == max_rank:
            print("rank saturation reached — stopping simulation at t =", t)
            break


if __name__ == "__main__":
    run_simulation()
