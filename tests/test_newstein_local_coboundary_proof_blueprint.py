from pathlib import Path

def test_newstein_local_coboundary_proof_blueprint_lock():
    s = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_PROOF_BLUEPRINT.md").read_text()
    assert "# Newstein Local Coboundary Proof Blueprint" in s
    assert "## Status\nOPEN" in s
    assert "Choose a rooted spanning forest" in s
    assert "fundamental cycle" in s
    assert "Weakest missing sublemma" in s
