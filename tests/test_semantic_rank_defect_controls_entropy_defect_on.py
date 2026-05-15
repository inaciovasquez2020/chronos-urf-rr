import subprocess
import sys

def test_semantic_rank_defect_controls_entropy_defect_on_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_semantic_rank_defect_controls_entropy_defect_on.py"],
        check=True,
    )
