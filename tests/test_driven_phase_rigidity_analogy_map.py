import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_driven_phase_rigidity_analogy_map_verifier():
    subprocess.run(
        ["python3", "tools/verify_driven_phase_rigidity_analogy_map.py"],
        cwd=ROOT,
        check=True,
    )
