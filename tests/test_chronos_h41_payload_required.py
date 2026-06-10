import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_chronos_h41_payload_required_verifier():
    subprocess.run(
        ["python3", "tools/verify_chronos_h41_payload_required.py"],
        cwd=ROOT,
        check=True,
    )
