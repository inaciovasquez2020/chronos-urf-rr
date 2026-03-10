import json
import matplotlib.pyplot as plt
from collections import defaultdict

with open("results/cor_scaling_regular.json") as f:
    data = json.load(f)

groups = defaultdict(list)

for row in data:
    groups[row["n"]].append(row["cor"])

xs=[]
ys=[]

for n,v in sorted(groups.items()):
    xs.append(n)
    ys.append(sum(v)/len(v))

plt.plot(xs,ys,marker="o")
plt.xlabel("n")
plt.ylabel("Average COR")
plt.title("Cycle Overlap Rank Scaling")
plt.savefig("results/cor_scaling.png")
plt.show()
