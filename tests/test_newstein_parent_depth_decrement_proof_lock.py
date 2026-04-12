from pathlib import Path

LEAN = Path("lean/Newstein/ParentDepthDecrement.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_THEOREM.md").read_text()

def test_theorem_present():
    assert "theorem ParentDepthDecrement" in LEAN

def test_axiom_forbidden():
    assert "axiom ParentDepthDecrement" not in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC
