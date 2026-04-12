from pathlib import Path

def test_newstein_fundamental_cycle_generation_proof_blueprint_lock():
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_PROOF_BLUEPRINT.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Proof Blueprint" in s
    assert "## Status\nOPEN" in s
    assert "Define the fundamental cycle" in s
    assert "rooted-local generating family" in s
    assert "Weakest missing sublemma" in s
