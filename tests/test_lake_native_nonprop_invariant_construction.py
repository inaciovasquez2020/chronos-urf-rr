import subprocess
import sys

def test_lake_native_nonprop_invariant_construction_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_lake_native_nonprop_invariant_construction.py"],
        check=True,
    )
