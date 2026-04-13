from pathlib import Path

def test_newstein_parent_iteration_depth_formula_theorem_lock() -> None:
    text = Path("docs/math/NEWSTEIN_PARENT_ITERATION_DEPTH_FORMULA_THEOREM.md").read_text(encoding="utf-8")
    assert "Status: PROVED" in text
    assert "d\\!\\left(\\eta^{\\,n}(v), r\\right)=d(v,r)-n" in text
    assert "\\eta^{\\,d(v,r)}(v)=r" in text
    assert "ParentIterationDepthFormula" in text
    assert "ParentIterationToRoot" in text
    assert "TreeContractionHomotopy" in text
    assert "RootedBallTrivialization" in text
    assert "weakest sufficient theorem-level replacement target" in text
    assert "Proved by induction using the one-step parent-depth decrement law." in text
