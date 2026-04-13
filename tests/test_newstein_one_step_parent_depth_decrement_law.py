from pathlib import Path

def test_newstein_one_step_parent_depth_decrement_law_lock() -> None:
    text = Path("docs/math/NEWSTEIN_ONE_STEP_PARENT_DEPTH_DECREMENT_LAW.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "d(\\eta(w),r)=d(w,r)-1" in text
    assert "w \\neq r" in text
    assert "unique nontrivial step input in the induction proof of ParentIterationDepthFormula" in text
