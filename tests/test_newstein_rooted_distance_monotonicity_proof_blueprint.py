from pathlib import Path

def test_newstein_rooted_distance_monotonicity_proof_blueprint_lock():
    s = Path("docs/math/NEWSTEIN_ROOTED_DISTANCE_MONOTONICITY_PROOF_BLUEPRINT.md").read_text()
    assert "# Newstein Rooted-Distance Monotonicity Proof Blueprint" in s
    assert "## Status\nOPEN" in s
    assert "depth by exactly one" in s
