import subprocess
import sys


def test_selected_domain_unconditional_closure_constructor_obligation_matrix_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_unconditional_closure_constructor_obligation_matrix_2026_06_24.py",
 ],
 check=True,
 )
