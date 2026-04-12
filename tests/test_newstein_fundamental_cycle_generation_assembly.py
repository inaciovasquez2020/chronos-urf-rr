from pathlib import Path

def test_newstein_fundamental_cycle_generation_assembly_locked():
    p = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Fundamental Cycle Generation Assembly" in s
    assert "## Status\nOPEN" in s
    assert "Let \\(e=\\{u,v\\}\\) be a non-tree edge." in s
    assert "C_T(e)=P_T(u,v)\\cup\\{e\\}" in s
    assert "## Assembly inputs" in s
    assert "Tree-path rooted locality assembly." in s
    assert "Definition of a fundamental cycle with respect to a spanning tree." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{FundamentalCycleGeneration}" in s
    assert "\\mathrm{LocalCoboundaryCriterion}" in s
