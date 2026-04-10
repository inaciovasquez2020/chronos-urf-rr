import json
from pathlib import Path
import subprocess, sys

def test_high_girth_base():
    subprocess.run([sys.executable, "scripts/generate_high_girth_base.py"], check=True)
    p = Path("artifacts/high_girth_base.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["girth"] >= data["target"]
