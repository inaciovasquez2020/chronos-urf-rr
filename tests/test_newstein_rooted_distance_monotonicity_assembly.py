from pathlib import Path

def test_newstein_rooted_distance_monotonicity_assembly_locked():
    p = Path("docs/math/NEWSTEIN_ROOTED_DISTANCE_MONOTONICITY_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Rooted-Distance Monotonicity Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{par}_T(u)=\\operatorname{par}_T(v)." in s
    assert "\\operatorname{depth}_T(u)=\\operatorname{depth}_T(v)." in s
    assert "## Assembly inputs" in s
    assert "Parent-depth decrement assembly." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{RootedDistanceMonotonicity}" in s
    assert "\\mathrm{OneStepParentStability}" in s
