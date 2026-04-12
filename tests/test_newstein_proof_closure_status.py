from pathlib import Path

def test_newstein_proof_closure_status_lock():
    s = Path("docs/status/NEWSTEIN_PROOF_CLOSURE_STATUS.md").read_text()
    assert "# Newstein Proof Closure Status" in s
    assert "## Solved" in s
    assert "## Locked frontier" in s
