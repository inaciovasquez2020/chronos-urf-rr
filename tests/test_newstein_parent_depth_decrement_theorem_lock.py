from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_THEOREM.md").read_text()

def test_title_present():
    assert "NEWSTEIN PARENT-DEPTH DECREMENT THEOREM" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_dependency_chain_present():
    assert "ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional" in DOC
