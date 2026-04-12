from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_THEOREM.md").read_text()

def test_title_present():
    assert "NEWSTEIN ROOTED-BALL TRIVIALIZATION THEOREM" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_parent_depth_dependency_present():
    assert "Assume the theorem-level parent-depth decrement result" in DOC

def test_dependency_chain_present():
    assert "ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional" in DOC
