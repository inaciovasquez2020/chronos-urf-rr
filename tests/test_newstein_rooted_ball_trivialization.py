from pathlib import Path


def test_newstein_rooted_ball_trivialization_lock():
    s = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION.md").read_text()
    assert "Newstein Rooted-Ball Trivialization" in s
    assert "Status: OPEN" in s
    assert "For every rooted ball" in s
    assert "chain homotopy or equivalent explicit contraction operator" in s
