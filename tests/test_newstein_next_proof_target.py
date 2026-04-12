from pathlib import Path

def test_newstein_next_proof_target_lock():
    s = Path("docs/math/NEWSTEIN_NEXT_PROOF_TARGET.md").read_text()
    assert "# Newstein Next Proof Target" in s
    assert "## Status\nOPEN" in s
    assert "Newstein Local Coboundary Criterion." in s
