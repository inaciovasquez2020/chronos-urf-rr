import subprocess
import sys


def test_selected_domain_final_closure_obligation_interface_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_final_closure_obligation_interface_2026_06_24.py",
 ],
 check=True,
 )
