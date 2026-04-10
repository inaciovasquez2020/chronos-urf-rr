from pathlib import Path

def test_betti_final_exists():
    s = Path("URF/Lean/Algebra/BettiFinal.lean").read_text()
    assert "betti_formula" in s
    assert "Z1" in s
    assert "boundary" in s
