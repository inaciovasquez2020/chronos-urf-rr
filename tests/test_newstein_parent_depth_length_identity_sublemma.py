from pathlib import Path

def test_newstein_parent_depth_length_identity_sublemma_locked():
    p = Path("docs/math/NEWSTEIN_PARENT_DEPTH_LENGTH_IDENTITY_SUBLEMMA.md")
    s = p.read_text()
    assert "# Newstein Parent-Depth Length Identity Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "For every non-root vertex \\(v\\)," in s
    assert "d_T(r,v)=d_T(r,\\operatorname{par}_T(v))+1" in s
    assert "## Proof skeleton" in s
    assert "This is the Step 3 input for the parent-depth decrement proof blueprint." in s
    assert "\\mathrm{ParentDepthLengthIdentity}" in s
    assert "\\mathrm{ParentDepthDecrement\\ proof}" in s
