from pathlib import Path

def test_newstein_parent_stability_to_geodesic_promotion_plan_lock():
    s = Path("docs/math/NEWSTEIN_PARENT_STABILITY_TO_GEODESIC_PROMOTION_PLAN.md").read_text()
    assert "# Newstein Parent-Stability-to-Geodesic Promotion Plan" in s
    assert "## Status\nOPEN" in s
    assert "NEWSTEIN_GEODESIC_INTERPOLATION_CLOSURE_SUBLEMMA.md" in s
