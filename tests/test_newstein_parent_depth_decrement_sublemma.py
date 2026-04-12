from pathlib import Path

def test_newstein_parent_depth_decrement_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_SUBLEMMA.md").read_text()
    assert "# Newstein Parent Depth Decrement Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{depth}_T(p)=\\operatorname{depth}_T(w)-1" in s
