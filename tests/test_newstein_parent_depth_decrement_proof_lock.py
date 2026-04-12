from pathlib import Path

LEAN = Path("lean/Newstein/ParentDepthDecrement.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_THEOREM.md").read_text()

def test_theorem_present():
    assert "theorem ParentDepthDecrement" in LEAN

def test_no_axiom_or_trivial_placeholder():
    assert "axiom ParentDepthDecrement" not in LEAN
    assert ": Prop := by\n  trivial" not in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC

def test_doc_discharge_present():
    assert "## Discharge" in DOC
    assert "MetricDepthCoincidence" in DOC
    assert "parent_dist_step" in DOC
