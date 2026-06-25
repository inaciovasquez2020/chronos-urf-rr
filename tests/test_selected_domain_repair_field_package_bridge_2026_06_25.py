from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_selected_domain_repair_field_package_bridge_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    verifier = root / "tools" / "verify_selected_domain_repair_field_package_bridge_2026_06_25.py"

    result = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_2026_06_25_OK" in result.stdout
