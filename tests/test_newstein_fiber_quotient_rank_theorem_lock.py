from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_THEOREM.md").read_text()

def test_title_present():
    assert "NEWSTEIN FIBER-QUOTIENT-RANK THEOREM" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_rooted_ball_dependency_present():
    assert "Assume the theorem-level rooted-ball trivialization result" in DOC

def test_dependency_chain_present():
    assert "ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional" in DOC
