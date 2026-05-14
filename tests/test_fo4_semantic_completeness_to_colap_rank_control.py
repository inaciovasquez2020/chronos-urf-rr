import subprocess
import sys

def test_fo4_semantic_completeness_to_colap_rank_control_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fo4_semantic_completeness_to_colap_rank_control.py"],
        check=True,
    )
