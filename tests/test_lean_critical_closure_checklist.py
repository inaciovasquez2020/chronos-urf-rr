from pathlib import Path

def test_lean_critical_closure_checklist_present():
    s = Path("docs/specs/LEAN_CRITICAL_CLOSURE_CHECKLIST.md").read_text()
    assert "define `IR : ℕ → Graph → ℕ`" in s
    assert "prove `localTwoComplexH1Rank_growth`" in s
    assert "package as `W5_rank_separation`" in s
    assert "zero `axiom`" in s
    assert "zero `sorry`" in s
    assert "zero `admit`" in s
    assert "The following remain outside unconditional graph-side closure" in s
