from pathlib import Path
import subprocess
import sys


def test_r1_native_map_input_contract_conditional_constructor_from_targets():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_native_map_input_contract_conditional_constructor_from_targets.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "R1_NATIVE_MAP_INPUT_CONTRACT_CONDITIONAL_CONSTRUCTOR_FROM_TARGETS_OK" in result.stdout
