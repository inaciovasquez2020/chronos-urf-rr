import subprocess
import sys


def test_selected_domain_defect_repair_interface_merge_readiness_verifier() -> None:
 subprocess.run(
 [
 sys.executable,
 "tools/verify_selected_domain_defect_repair_interface_merge_readiness_2026_06_24.py",
 ],
 check=True,
 )
