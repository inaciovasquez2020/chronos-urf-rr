import subprocess
import sys


def test_selected_domain_final_conditional_closure_toolkit_status_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_final_conditional_closure_toolkit_status_2026_06_24.py",
 ],
 check=True,
 )
