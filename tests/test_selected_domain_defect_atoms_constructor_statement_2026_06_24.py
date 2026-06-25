import subprocess
import sys


def test_selected_domain_defect_atoms_constructor_statement_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_defect_atoms_constructor_statement_2026_06_24.py",
 ],
 check=True,
 )
