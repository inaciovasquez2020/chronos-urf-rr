from pathlib import Path

def test_newstein_tree_contraction_homotopy_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_TREE_CONTRACTION_HOMOTOPY_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: PROVED" in text
    assert "\\eta^{\\,d(v,r)}(v)=r" in text
    assert "H(v,t):=\\eta^{\\,\\min(t,d(v,r))}(v)" in text
    assert "H(v,0)=v" in text
    assert "H(v,R)=r" in text
    assert "TreeContractionHomotopy is reduced to constructing the chain-level extension of the parent-iteration-to-root map" in text
    assert "Proved by constructing the chain-level extension of the parent-iteration-to-root map \\(H\\)." in text
