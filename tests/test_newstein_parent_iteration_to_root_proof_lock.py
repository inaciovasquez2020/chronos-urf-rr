from pathlib import Path

DOC = Path("docs/math/NEWSTEIN_PARENT_ITERATION_TO_ROOT_THEOREM.md").read_text()


def test_theorem_target_present():
    assert "# Newstein Parent-Iteration-to-Root Theorem" in DOC
    assert "Status: PROVED" in DOC


def test_dependency_chain_present():
    assert "FiberQuotientRank^thm" in DOC
    assert "PerStepInformationBound^thm" in DOC
    assert "QuotientGapClosure^unconditional" in DOC
