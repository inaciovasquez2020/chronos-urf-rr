from pathlib import Path

LEAN = Path("lean/Newstein/PerStepInformationBound.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND_THEOREM.md").read_text()

def test_theorem_present():
    assert "theorem PerStepInformationBound" in LEAN

def test_axiom_forbidden():
    assert "axiom PerStepInformationBound" not in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC
