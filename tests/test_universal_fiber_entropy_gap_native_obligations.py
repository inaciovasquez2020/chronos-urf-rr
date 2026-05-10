import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_universal_fiber_entropy_gap_native_obligations_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_universal_fiber_entropy_gap_native_obligations.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "UniversalFiberEntropyGap native obligations verified." in result.stdout
