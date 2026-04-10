from pathlib import Path

def test_cycle_space_present():
    s = Path("URF/Lean/Algebra/CycleSpace.lean").read_text()
    assert "def boundary" in s
    assert "def Z1" in s
    assert "FinGraph" in s
    assert "ZMod 2" in s
