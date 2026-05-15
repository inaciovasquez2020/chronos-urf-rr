import subprocess
import sys

def test_canonical_to_nontrivial_strengthening_for_predicate_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_canonical_to_nontrivial_strengthening_for_predicate.py"],
        check=True,
    )
