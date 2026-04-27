import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_theorem_level_frontiers_status_lock():
    p = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_theorem_level_frontiers.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert p.returncode == 0, p.stderr + p.stdout
    assert "PASS: theorem-level frontiers remain explicitly conditional" in p.stdout
