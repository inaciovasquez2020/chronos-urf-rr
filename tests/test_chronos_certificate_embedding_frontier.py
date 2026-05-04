import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_chronos_certificate_embedding_frontier_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_chronos_certificate_embedding_frontier.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "FRONTIER_OPEN" in result.stdout
