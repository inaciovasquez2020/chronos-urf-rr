import subprocess
import numpy as np

deltas = [4,6,8,10]
lambdas = [0.05,0.1,0.2,0.3]

for Δ in deltas:
    for λ in lambdas:
        cmd = f"python3 toolkit/ogp/ogp_curvature_solver.py {Δ} {λ}"
        print(cmd)
