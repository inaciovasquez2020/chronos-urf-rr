import subprocess
import sys


def test_selected_domain_construction_input_witness_reduction_statement_verifier() -> None:
    subprocess.run(
        [
            sys.executable,
            "tools/verify_selected_domain_construction_input_witness_reduction_statement_2026_06_25.py",
        ],
        check=True,
    )
