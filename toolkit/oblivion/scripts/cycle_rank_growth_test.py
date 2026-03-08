#!/usr/bin/env python3
import json
import numpy as np

with open("toolkit/oblivion/results/cycle_rank_scaling.json") as f:
    data=json.load(f)

n=np.array([d["n"] for d in data])
rank=np.array([d["rank_F2"] for d in data])

ratio=rank/n

print("n:",n.tolist())
print("rank:",rank.tolist())
print("rank/n:",ratio.tolist())

# linear regression rank ≈ a*n + b
A=np.vstack([n,np.ones(len(n))]).T
a,b=np.linalg.lstsq(A,rank,rcond=None)[0]

print("linear_fit_slope:",float(a))
print("linear_fit_intercept:",float(b))

if a>0.1:
    print("RESULT: empirical linear rank growth detected")
else:
    print("RESULT: rank growth sublinear")
