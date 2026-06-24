import subprocess
import sys


def test_selected_domain_unconditional_closure_construction_input_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_unconditional_closure_construction_input_2026_06_24.py",
 ],
 check=True,
 )
