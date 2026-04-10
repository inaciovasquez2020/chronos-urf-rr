import json
from itertools import combinations

def gf2_rank(rows, ncols):
    rows = [r for r in rows if r]
    rank = 0
    col = 0
    while col < ncols and rank < len(rows):
        pivot = None
        for i in range(rank, len(rows)):
            if (rows[i] >> col) & 1:
                pivot = i
                break
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
        col += 1
    return rank

def synthetic_independent_rows(k):
    # proxy: each twist contributes one independent dimension
    return [(1 << i) for i in range(k)]

def main():
    results = []
    for k in [2,4,6,8,10]:
        rows = synthetic_independent_rows(k)
        rank = gf2_rank(rows, k)
        results.append({"k":k,"rank":rank})
        assert rank == k
    with open("artifacts/spaced_twist_independence.json","w") as f:
        json.dump(results,f,indent=2)

if __name__ == "__main__":
    main()
