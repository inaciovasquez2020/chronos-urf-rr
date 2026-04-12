from pathlib import Path

def test_newstein_fiber_quotient_rank_lock():
    s = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK.md").read_text()
    assert "# Newstein Fiber Quotient Rank" in s
    assert "## Status" in s
    assert "OPEN" in s
    assert "Minimal sufficient assumption" in s
    assert "Z_1(B_R(r)) / B_1(B_R(r))" in s
    assert "\\operatorname{rank} Q(B_R(r)) = 0." in s
    assert "DirectSumIndependence" in s
