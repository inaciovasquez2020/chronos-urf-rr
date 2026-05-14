import subprocess
import sys

def test_fo4_semantic_completeness_surface_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fo4_semantic_completeness_surface.py"],
        check=True,
    )
