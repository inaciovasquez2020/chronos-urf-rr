import subprocess
import sys


def test_selected_domain_defect_atoms_constructor_target_witness_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_defect_atoms_constructor_target_witness_2026_06_25.py",
 ],
 check=True,
 )
