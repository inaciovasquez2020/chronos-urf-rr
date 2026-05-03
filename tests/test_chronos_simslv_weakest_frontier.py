import subprocess
import sys
from pathlib import Path

def test_chronos_simslv_weakest_frontier_verifier_passes():
    result = subprocess.run(
        [sys.executable, "scripts/verify_chronos_simslv_weakest_frontier.py"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "PASS" in result.stdout

def test_chronos_simslv_weakest_frontier_boundary_language():
    doc = Path("docs/status/CHRONOS_SIMSLV_WEAKEST_FRONTIER_LEMMA_2026_05_03.md").read_text()
    assert "CONDITIONAL_FRONTIER" in doc
    assert "FRONTIER_OPEN" in doc
    assert "does not assert unconditional Chronos closure" in doc
    assert "does not assert theorem-level H4.1/FGL closure" in doc
    assert "FRONTIER_CLOSED" not in doc
