from pathlib import Path

def test_newstein_proof_closure_status_lock():
    s = Path("docs/status/NEWSTEIN_PROOF_CLOSURE_STATUS.md").read_text()
    assert "# Newstein Proof Closure Status" in s
    assert "## Status\nOPEN" in s
    assert "Registry closure\nCOMPLETE" in s
    assert "Proof closure\nOPEN" in s
    assert "Newstein Local Coboundary Criterion." in s
