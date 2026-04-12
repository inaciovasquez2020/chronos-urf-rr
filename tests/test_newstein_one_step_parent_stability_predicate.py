from pathlib import Path

def test_newstein_one_step_parent_stability_predicate_lock():
    s = Path("docs/math/NEWSTEIN_ONE_STEP_PARENT_STABILITY_PREDICATE.md").read_text()
    assert "# Newstein One-Step Parent Stability Predicate" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{par}_T(w)\\in B_R(v)" in s
    assert "atomic predicate" in s
