from pathlib import Path

def test_newstein_fundamental_cycle_to_local_coboundary_promotion_lock():
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_TO_LOCAL_COBOUNDARY_PROMOTION.md").read_text()
    assert "# Newstein Fundamental-Cycle-to-Local-Coboundary Promotion" in s
    assert "## Status\nOPEN" in s
    assert "is a coboundary on \\(B_R(v)\\)" in s
