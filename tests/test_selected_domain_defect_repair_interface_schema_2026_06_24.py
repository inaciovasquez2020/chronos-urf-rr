import subprocess
import sys

def test_selected_domain_defect_repair_interface_schema_verifier() -> None: subprocess.run([sys.executable, "tools/verify_selected_domain_defect_repair_interface_schema_2026_06_24.py"], check=True)
