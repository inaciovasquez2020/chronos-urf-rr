from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_THEOREM.md").read_text()
LEAN = Path("lean/Newstein/ParentDepthDecrement.lean").read_text()

def test_status_proved_present():
    assert "Status: PROVED" in DOC

def test_metric_bridge_present():
    assert "HasMetricDepthCoincidence" in LEAN
    assert "metric_depth_coincidence" in LEAN

def test_parent_step_present():
    assert "HasParentDistStep" in LEAN
    assert "parent_in_ball" in LEAN
    assert "parent_dist_step" in LEAN

def test_typed_theorem_present():
    assert "theorem ParentDepthDecrement" in LEAN
    assert "depth_G (parent_G x) = depth_G x - 1" in LEAN

def test_rewrite_chain_present():
    assert "rw [hM.metric_depth_coincidence (parent_G x)" in LEAN
    assert "rw [hM.metric_depth_coincidence x hxb]" in LEAN
    assert "exact hP.parent_dist_step x hx hxb" in LEAN

def test_dependency_chain_present():
    assert "ParentDepthDecrement^proved => RootedBallTrivialization^conditional => FiberQuotientRank^conditional => DirectSumIndependence^conditional => PerStepInformationBound^conditional => QuotientGapClosure^conditional" in DOC
