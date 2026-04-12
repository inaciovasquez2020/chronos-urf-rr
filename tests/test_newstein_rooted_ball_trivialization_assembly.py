from pathlib import Path

def test_newstein_rooted_ball_trivialization_assembly_locked():
    p = Path("docs/math/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Rooted-Ball Trivialization Assembly" in s
    assert "## Status\nOPEN" in s
    assert "the rooted ball trivializes after passage to the local coboundary quotient" in s
    assert "## Assembly inputs" in s
    assert "Local coboundary criterion assembly." in s
    assert "Definition of the local quotient by rooted-local coboundaries." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{RootedBallTrivialization}" in s
    assert "\\mathrm{FiberQuotientRank}" in s
