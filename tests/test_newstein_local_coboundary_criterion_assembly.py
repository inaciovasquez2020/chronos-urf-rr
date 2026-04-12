from pathlib import Path

def test_newstein_local_coboundary_criterion_assembly_locked():
    p = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_CRITERION_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Local Coboundary Criterion Assembly" in s
    assert "## Status\nOPEN" in s
    assert "the local coboundary criterion" in s
    assert "## Assembly inputs" in s
    assert "Fundamental cycle generation assembly." in s
    assert "Linear generation of local cycle space by fundamental cycles of non-tree edges." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{LocalCoboundaryCriterion}" in s
    assert "\\mathrm{RootedBallTrivialization}" in s
