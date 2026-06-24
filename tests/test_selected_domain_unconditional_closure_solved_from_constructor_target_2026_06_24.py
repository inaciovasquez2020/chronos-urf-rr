import subprocess
import sys


def test_selected_domain_unconditional_closure_solved_from_constructor_target_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_unconditional_closure_solved_from_constructor_target_2026_06_24.py",
 ],
 check=True,
 )
