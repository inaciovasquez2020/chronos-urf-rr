#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "experiments" / "cycle_rank_test.py"
OUT  = ROOT / "results" / "cycle_rank_batch.json"

runs = []

for n in [200,400,800,1200]:
    for d in [3,4,5]:
        p = subprocess.run(
            ["python3", str(TEST)],
            capture_output=True,
            text=True
        )
        lines = p.stdout.splitlines()
        m = None
        r = None
        ratio = None
        for L in lines:
            if L.startswith("cycles:"):
                m = int(L.split(":")[1].strip())
            if L.startswith("rank:"):
                r = int(L.split(":")[1].strip())
            if L.startswith("rank/m:"):
                ratio = float(L.split(":")[1].strip())
        runs.append({
            "n": n,
            "d": d,
            "cycles": m,
            "rank": r,
            "ratio": ratio
        })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(runs, indent=2))

print("saved:", OUT)
