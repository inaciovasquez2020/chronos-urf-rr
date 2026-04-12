from pathlib import Path

LEAN = Path("lean/Newstein/DirectSumIndependence.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_DIRECT_SUM_INDEPENDENCE_THEOREM.md").read_text()

def test_theorem_present():
    assert "theorem DirectSumIndependence" in LEAN

def test_axiom_forbidden():
    assert "axiom DirectSumIndependence" not in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC
