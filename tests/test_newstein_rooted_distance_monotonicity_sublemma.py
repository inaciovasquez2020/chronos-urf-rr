from pathlib import Path

def test_newstein_rooted_distance_monotonicity_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_ROOTED_DISTANCE_MONOTONICITY_SUBLEMMA.md").read_text()
    assert "# Newstein Rooted-Distance Monotonicity Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "d(v,p)\\le d(v,w)" in s
