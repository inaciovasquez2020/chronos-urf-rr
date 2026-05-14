import subprocess
import sys

def test_lake_native_fiber_large_from_nonprop_core_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_lake_native_fiber_large_from_nonprop_core.py"],
        check=True,
    )
