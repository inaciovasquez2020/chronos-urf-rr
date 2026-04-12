from pathlib import Path

def test_newstein_rooted_ball_trivialization_lock():
    s = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION.md").read_text()
    assert "# Newstein Rooted Ball Trivialization" in s
    assert "## Status" in s
    assert "OPEN" in s
    assert "Minimal sufficient assumption" in s
    assert "partial h + h partial" not in s
    assert "\\partial h + h \\partial = \\mathrm{Id} - \\mathrm{Retr}_r." in s
    assert "Z_k(B_R(r)) = B_k(B_R(r))" in s
    assert "RootedBallTrivialization" in s
    assert "FiberQuotientRank" in s
