import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ball_cycle_axiom_quarantine_status_lock():
    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_ball_cycle_axiom_quarantine.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout
    assert "PASS: ball-cycle-length axiom is quarantined" in p.stdout
