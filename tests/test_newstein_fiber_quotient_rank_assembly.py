from pathlib import Path

def test_newstein_fiber_quotient_rank_assembly_locked():
    p = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Fiber Quotient-Rank Assembly" in s
    assert "## Status\nOPEN" in s
    assert "the global quotient rank is determined entirely by the surviving inter-fiber classes" in s
    assert "## Assembly inputs" in s
    assert "Rooted-ball trivialization assembly." in s
    assert "Additivity of rank under quotient decomposition into trivial and surviving parts." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{FiberQuotientRank}" in s
    assert "\\mathrm{DirectSumIndependence}" in s
