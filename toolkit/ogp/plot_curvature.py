import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("toolkit/ogp/results/bethe_curvature_scan.csv")

for d in sorted(df["Δ"].unique()):
    sub = df[df["Δ"]==d]
    plt.plot(sub["λ"], sub["curvature"], marker="o", label=f"Δ={d}")

plt.xlabel("λ")
plt.ylabel("curvature")
plt.legend()
plt.tight_layout()
plt.savefig("toolkit/ogp/results/curvature_plot.png")
