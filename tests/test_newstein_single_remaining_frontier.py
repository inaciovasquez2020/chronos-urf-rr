from pathlib import Path

def test_newstein_single_remaining_frontier_lock() -> None:
    text = Path("docs/status/NEWSTEIN_SINGLE_REMAINING_FRONTIER.md").read_text(encoding="utf-8")
    assert "Status: CONDITIONAL" in text
    assert "OneStepParentDepthDecrement" in text
    assert "w \\neq r \\Longrightarrow d(\\eta(w),r)=d(w,r)-1" in text
    assert "ParentIterationDepthFormula" in text
    assert "ParentIterationToRoot" in text
    assert "TreeContractionHomotopy" in text
    assert "RootedBallTrivialization" in text
    assert "LocalCoboundaryCriterion" in text
    assert "FiberToGlobalInjection" in text
    assert "AssemblyTheorem" in text
    assert "unique remaining frontier after reduction completion" in text
