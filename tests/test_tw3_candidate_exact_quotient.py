import subprocess
import sys

def test_tw3_candidate_exact_quotient():
    proc = subprocess.run(
        [sys.executable, "scripts/verify_tw3_candidate_exact_quotient.py", "2", "5"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "exact_quotient_rank:" in proc.stdout
