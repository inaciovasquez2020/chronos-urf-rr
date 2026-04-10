import json, subprocess, sys
from pathlib import Path

def test_gap_full():
    subprocess.run([sys.executable,"scripts/verify_family_gap_full.py"],check=True)
    data = json.loads(Path("artifacts/family_gap_full.json").read_text())
    assert data[-1]["gap"] > data[0]["gap"]
