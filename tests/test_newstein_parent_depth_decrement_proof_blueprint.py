from pathlib import Path

def test_newstein_parent_depth_decrement_proof_blueprint_locked():
    p = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_PROOF_BLUEPRINT.md")
    s = p.read_text()
    assert "# Newstein Parent Depth Decrement Proof Blueprint" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T(v))=\\operatorname{depth}_T(v)-1" in s
    assert "### Step 1" in s
    assert "### Step 2" in s
    assert "### Step 3" in s
    assert "### Step 4" in s
    assert "\\mathrm{ParentDepthDecrement\\ proof}" in s
    assert "\\mathrm{RootedDistanceMonotonicity}" in s
