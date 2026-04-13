from pathlib import Path

def test_newstein_exact_missing_object_lock():
    text = Path("docs/math/NEWSTEIN_EXACT_MISSING_OBJECT.md").read_text(encoding="utf-8")
    assert "\\Phi_m(x_0,\\dots,x_m)" in text
    assert "\\forall I\\subseteq\\{0,\\dots,m\\}" in text
    assert "\\text{Status}=\\text{OPEN}." in text

def test_newstein_rooted_ball_trivialization_status_lock():
    text = Path("docs/status/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_STATUS.md").read_text(encoding="utf-8")
    assert "\\text{Status}=\\text{OPEN-FRONTIER}." in text
    assert "NEWSTEIN_EXACT_MISSING_OBJECT.md" in text
    assert "No unconditional proof closure is claimed in the repository." in text
