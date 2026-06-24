import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_selected_domain_defect_basis_branch_merge_readiness_2026_06_24.py"

def test_selected_domain_defect_basis_branch_merge_readiness_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "SELECTED_DOMAIN_DEFECT_BASIS_BRANCH_MERGE_READINESS_2026_06_24_OK" in result.stdout
