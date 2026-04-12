from pathlib import Path

def test_newstein_parent_depth_decrement_proof_target_locked():
    p = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_PROOF_TARGET.md")
    s = p.read_text()
    assert "# Newstein Parent Depth Decrement Proof Target" in s
    assert "## Status\nOPEN" in s
    assert "operatorname{depth}_T(\\operatorname{par}_T(v)) = \\operatorname{depth}_T(v) - 1" in s
    assert "This theorem discharges the remaining gap in rooted-distance monotonicity" in s
    assert "\\mathrm{ParentDepthDecrement\\ proof}" in s
    assert "\\mathrm{RootedDistanceMonotonicity}" in s
