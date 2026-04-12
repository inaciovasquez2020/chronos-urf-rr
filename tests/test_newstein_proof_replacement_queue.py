from pathlib import Path

def test_newstein_proof_replacement_queue_lock():
    s = Path("docs/status/NEWSTEIN_PROOF_REPLACEMENT_QUEUE.md").read_text()
    assert "# Newstein Proof Replacement Queue" in s
    assert "## Status\nOPEN" in s
    assert "Canonical next replacement" in s
    assert "Newstein Local Coboundary Criterion." in s
