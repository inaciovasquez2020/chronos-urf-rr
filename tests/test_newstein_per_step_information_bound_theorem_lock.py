from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND_THEOREM.md").read_text()

def test_title_present():
    assert "NEWSTEIN PER-STEP-INFORMATION-BOUND THEOREM" in DOC

def test_status_open_present():
    assert "Status: OPEN" in DOC

def test_direct_sum_dependency_present():
    assert "Assume the theorem-level direct-sum-independence result" in DOC

def test_dependency_chain_present():
    assert "ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional" in DOC
