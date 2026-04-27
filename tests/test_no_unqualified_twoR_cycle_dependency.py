import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_no_unqualified_twoR_cycle_dependency():
    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_no_unqualified_twoR_cycle_dependency.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout
    assert "PASS: unqualified 2R cycle-length dependency removed" in p.stdout
