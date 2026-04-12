from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_DIRECT_SUM_INDEPENDENCE_THEOREM.md").read_text()

def test_title_present():
    assert "NEWSTEIN DIRECT-SUM-INDEPENDENCE THEOREM" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_fiber_rank_dependency_present():
    assert "Assume the theorem-level fiber-quotient-rank result" in DOC

def test_dependency_chain_present():
    assert "ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional" in DOC
