from pathlib import Path

def test_newstein_one_step_parent_stability_proof_blueprint_lock():
    s = Path("docs/math/NEWSTEIN_ONE_STEP_PARENT_STABILITY_PROOF_BLUEPRINT.md").read_text()
    assert "# Newstein One-Step Parent Stability Proof Blueprint" in s
    assert "## Status\nOPEN" in s
    assert "nonincreasing under one-step parent iteration" in s
    assert "d(v,\\operatorname{par}_T(w)) \\le d(v,w)" in s
