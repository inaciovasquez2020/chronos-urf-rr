import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_selected_domain_universal_gap_from_restricted_carrier_verifier():
    subprocess.run(
        ["python3", "tools/verify_selected_domain_universal_gap_from_restricted_carrier.py"],
        cwd=ROOT,
        check=True,
    )
