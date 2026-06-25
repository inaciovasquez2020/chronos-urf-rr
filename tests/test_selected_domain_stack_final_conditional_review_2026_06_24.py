import subprocess
import sys


def test_selected_domain_stack_final_conditional_review_verifier() -> None:
    subprocess.run(
        [
            sys.executable,
            "tools/verify_selected_domain_stack_final_conditional_review_2026_06_24.py",
        ],
        check=True,
    )
