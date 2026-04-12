from pathlib import Path

def test_newstein_local_coboundary_criterion_lock():
    s = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_CRITERION.md").read_text()
    assert "# Newstein Local Coboundary Criterion" in s
    assert "## Status\nOPEN" in s
    assert "Then \\(\\omega\\) is a coboundary on \\(B_R(v)\\)." in s
