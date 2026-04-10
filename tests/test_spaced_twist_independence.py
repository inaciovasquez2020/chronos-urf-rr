import json, subprocess, sys
from pathlib import Path

def test_independence():
    subprocess.run([sys.executable,"scripts/verify_spaced_twists_independence.py"],check=True)
    data = json.loads(Path("artifacts/spaced_twist_independence.json").read_text())
    assert all(d["rank"] == d["k"] for d in data)
