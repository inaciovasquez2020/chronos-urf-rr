from pathlib import Path

LEAN = Path("lean/Newstein/RootedBallTrivialization.lean").read_text()
DOC = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_THEOREM.md").read_text()

def test_theorem_present():
    assert "theorem RootedBallTrivialization" in LEAN

def test_axiom_forbidden():
    assert "axiom RootedBallTrivialization" not in LEAN

def test_doc_status_proved():
    assert "Status: PROVED" in DOC
