from pathlib import Path

def test_betti_number_present():
    s = Path("URF/Lean/Algebra/BettiNumber.lean").read_text()
    assert "beta1" in s
    assert "edgeCount" in s
    assert "vertexCount" in s
    assert "beta1_formula_tree_like" in s
