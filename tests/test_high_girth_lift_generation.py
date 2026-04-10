import json
from pathlib import Path
import subprocess
import sys

def test_generation():
    subprocess.run([sys.executable,"scripts/generate_high_girth_lift.py"],check=True)
    p = Path("artifacts/high_girth_lift.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert "edges" in data
    assert len(data["edges"]) > 0
