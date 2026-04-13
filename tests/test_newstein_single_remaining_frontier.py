from pathlib import Path

def test_newstein_single_remaining_frontier_lock() -> None:
    text = Path("docs/status/NEWSTEIN_SINGLE_REMAINING_FRONTIER.md").read_text(encoding="utf-8")
    assert "Status: RESOLVED" in text
    assert "previously recorded single remaining frontier `OneStepParentDepthDecrement` has been proved" in text
    assert "ParentIterationDepthFormula" in text
    assert "ParentIterationToRoot" in text
    assert "TreeContractionHomotopy" in text
    assert "RootedBallTrivialization" in text
    assert "LocalCoboundaryCriterion" in text
    assert "FiberToGlobalInjection" in text
    assert "AssemblyTheorem" in text
    assert "There is no remaining Newstein theorem-level frontier in this chain." in text
