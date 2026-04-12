from pathlib import Path

def test_newstein_one_step_parent_stability_assembly_locked():
    p = Path("docs/math/NEWSTEIN_ONE_STEP_PARENT_STABILITY_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein One-Step Parent Stability Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{par}_T(u)=\\operatorname{par}_T(v)." in s
    assert "same one-step parent layer" in s
    assert "## Assembly inputs" in s
    assert "Rooted-distance monotonicity assembly." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{OneStepParentStability}" in s
    assert "\\mathrm{ParentIterationClosure}" in s
