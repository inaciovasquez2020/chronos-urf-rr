import json
from pathlib import Path
import subprocess
import sys

def test_heawood_lift_pair():
    subprocess.run([sys.executable, "scripts/generate_heawood_lifts.py"], check=True)
    p = Path("artifacts/heawood_lift_pair_r2.json")
    assert p.exists()
    data = json.loads(p.read_text())

    assert data["base_name"] == "HeawoodGraph"
    assert data["radius"] == 2
    assert data["base_girth"] == 6

    cert = data["local_certificate"]
    assert cert["radius"] == 2
    assert cert["all_roots_isomorphic"] is True
    assert all(c["isomorphic"] is True for c in cert["certificates"])

    assert data["G_plus"]["local_cycle_length_bound"] == 5
    assert data["G_minus"]["local_cycle_length_bound"] == 5
