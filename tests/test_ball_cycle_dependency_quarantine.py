import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ball_cycle_dependency_quarantine_status_lock():
    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_ball_cycle_dependency_quarantine.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout
    assert "PASS: dependent 2R cycle-length usage is quarantined" in p.stdout
