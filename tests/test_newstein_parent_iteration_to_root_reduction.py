from pathlib import Path

def test_newstein_parent_iteration_to_root_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_PARENT_ITERATION_TO_ROOT_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: PROVED" in text
    assert "d\\!\\left(\\eta^{\\,n}(v),r\\right)=d(v,r)-n" in text
    assert "\\eta^{\\,d(v,r)}(v)=r" in text
    assert "Set \\(n=d(v,r)\\)." in text
    assert "d\\!\\left(\\eta^{\\,d(v,r)}(v),r\\right)=d(v,r)-d(v,r)=0." in text
    assert "distance \\(0\\) from \\(r\\) if and only if it is \\(r\\)" in text
    assert "ParentIterationToRoot is reduced to ParentIterationDepthFormula plus the identity-of-indiscernibles for graph distance." in text
    assert "Proved by specializing ParentIterationDepthFormula to \\(n=d(v,r)\\)." in text
