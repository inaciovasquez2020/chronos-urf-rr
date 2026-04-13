from pathlib import Path

def test_newstein_reduction_completion_status_lock() -> None:
    text = Path("docs/status/NEWSTEIN_REDUCTION_COMPLETION_STATUS.md").read_text(encoding="utf-8")
    assert "Status: CONDITIONAL" in text
    assert "The Newstein reduction chain is fully locked." in text
    assert "ParentIterationDepthFormula" in text
    assert "ParentIterationToRoot" in text
    assert "TreeContractionHomotopy" in text
    assert "RootedBallTrivialization" in text
    assert "LocalCoboundaryCriterion" in text
    assert "FiberToGlobalInjection" in text
    assert "AssemblyTheorem" in text
    assert "w \\neq r \\Longrightarrow d(\\eta(w),r)=d(w,r)-1" in text
    assert "Reduction-complete does not mean proof-complete." in text
