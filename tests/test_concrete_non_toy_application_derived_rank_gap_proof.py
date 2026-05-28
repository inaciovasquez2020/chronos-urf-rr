import subprocess
import sys

def test_concrete_non_toy_application_derived_rank_gap_proof():
    subprocess.run([sys.executable, "tools/verify_concrete_non_toy_application_derived_rank_gap_proof.py"], check=True)
