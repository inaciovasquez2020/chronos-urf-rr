import subprocess
import sys


def test_selected_domain_unconditional_construction_input_witness_missing_verifier() -> None:
    subprocess.run(
        [
            sys.executable,
            "tools/verify_selected_domain_unconditional_construction_input_witness_missing_2026_06_25.py",
        ],
        check=True,
    )
