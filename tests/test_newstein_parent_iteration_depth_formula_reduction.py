from pathlib import Path

def test_newstein_parent_iteration_depth_formula_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_PARENT_ITERATION_DEPTH_FORMULA_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "w \\neq r \\Longrightarrow d(\\eta(w),r)=d(w,r)-1" in text
    assert "d\\!\\left(\\eta^{\\,n}(v),r\\right)=d(v,r)-n" in text
    assert "The proof is by induction on \\(n\\)." in text
    assert "d\\!\\left(\\eta^{\\,0}(v),r\\right)=d(v,r)." in text
    assert "\\eta^{\\,n}(v)\\neq r" in text
    assert "ParentIterationDepthFormula is reduced to induction plus the one-step decrement law." in text
