from pathlib import Path

def test_newstein_geodesic_interpolation_closure_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_GEODESIC_INTERPOLATION_CLOSURE_SUBLEMMA.md").read_text()
    assert "# Newstein Geodesic Interpolation Closure Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "tree-convex" in s
    assert "fundamental cycle" in s
