import json, subprocess, sys
from pathlib import Path

def test_gap_growth():
    subprocess.run([sys.executable,"scripts/verify_heawood_family_gap.py"],check=True)
    data = json.loads(Path("artifacts/heawood_family_gap.json").read_text())
    gaps = [d["gap"] for d in data]
    assert all(gaps[i] <= gaps[i+1] for i in range(len(gaps)-1))
    assert gaps[-1] > gaps[0]
