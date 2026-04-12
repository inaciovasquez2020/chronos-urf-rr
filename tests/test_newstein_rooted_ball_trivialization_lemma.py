from pathlib import Path

def test_newstein_rooted_ball_trivialization_lock():
    s = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_LEMMA.md").read_text()
    assert "# Newstein Rooted-Ball Trivialization Lemma" in s
    assert "## Status\nOPEN" in s
    assert "Q_R(v)=0" in s
