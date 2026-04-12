from pathlib import Path

LEAN = Path("lean/Newstein/FiberQuotientRank.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_THEOREM.md").read_text()

def test_theorem_present():
    assert "theorem FiberQuotientRank" in LEAN

def test_axiom_forbidden():
    assert "axiom FiberQuotientRank" not in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC
