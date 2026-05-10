import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_open_frontier_status_snapshot_verifier():
    subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_open_frontier_status_snapshot.py")],
        cwd=ROOT,
        check=True,
    )
