from pathlib import Path

def test_newstein_lca_interpolation_closure_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_LCA_INTERPOLATION_CLOSURE_SUBLEMMA.md").read_text()
    assert "# Newstein LCA Interpolation Closure Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "least-common-ancestor interpolation" in s
