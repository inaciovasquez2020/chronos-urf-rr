import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_selected_domain_h41_fgl_from_chronos_rr_verifier():
    subprocess.run(
        ["python3", "tools/verify_selected_domain_h41_fgl_from_chronos_rr.py"],
        cwd=ROOT,
        check=True,
    )
