#!/usr/bin/env python3
import json
import matplotlib.pyplot as plt
import numpy as np

with open("toolkit/oblivion/results/cycle_rank_scaling.json") as f:
    data=json.load(f)

n=np.array([d["n"] for d in data])
rank=np.array([d["rank_F2"] for d in data])

plt.scatter(n,rank)
plt.plot(n,rank)
plt.xlabel("n")
plt.ylabel("rank_F2(M_R)")
plt.title("Cycle Incidence Rank Growth")
plt.savefig("toolkit/oblivion/results/cycle_rank_growth.png")
print("saved toolkit/oblivion/results/cycle_rank_growth.png")
