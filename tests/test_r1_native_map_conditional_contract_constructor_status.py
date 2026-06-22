from pathlib import Path
import subprocess
import sys


def test_r1_native_map_conditional_contract_constructor_status():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_native_map_conditional_contract_constructor_status.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_NATIVE_MAP_CONDITIONAL_CONTRACT_CONSTRUCTOR_STATUS_OK" in result.stdout
