from pathlib import Path

def test_newstein_rooted_ball_trivialization_reduction_lock() -> None:
    text = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_REDUCTION.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "\\partial h + h \\partial = \\operatorname{Id} - \\operatorname{Retr}_r" in text
    assert "every \\(1\\)-cycle" in text
    assert "z = \\partial h(z) + \\operatorname{Retr}_r(z)." in text
    assert "z=\\partial h(z)." in text
    assert "the root complex has no nontrivial \\(1\\)-simplices" in text
    assert "RootedBallTrivialization is reduced to TreeContractionHomotopy plus the vanishing of \\(1\\)-chains on the root retract." in text
