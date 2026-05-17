import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_selected_domain_chronos_rr_from_universal_gap_verifier():
    subprocess.run(
        ["python3", "tools/verify_selected_domain_chronos_rr_from_universal_gap.py"],
        cwd=ROOT,
        check=True,
    )
