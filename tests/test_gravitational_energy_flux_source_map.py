import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_gravitational_energy_flux_source_map_verifier():
    subprocess.run(
        ["python3", "tools/verify_gravitational_energy_flux_source_map.py"],
        cwd=ROOT,
        check=True,
    )
