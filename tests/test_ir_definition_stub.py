from pathlib import Path

def test_ir_definition_stub_present():
    s = Path("URF/Lean/Cycle/IR_Definition.lean").read_text()
    assert "def IR" in s
    assert "IR_iso_invariant" in s
    assert "LocalCycleSpan" in s
