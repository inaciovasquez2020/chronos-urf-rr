import json
from pathlib import Path
import subprocess, sys

def test_heawood_family():
    subprocess.run([sys.executable,"scripts/generate_heawood_family.py"],check=True)
    p = Path("artifacts/heawood_family_summary.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["blocks"] >= 1
    assert data["num_twists"] > 0
    assert data["expected_gap_lower_bound"] == data["num_twists"]
