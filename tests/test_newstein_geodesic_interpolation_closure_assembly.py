from pathlib import Path

def test_newstein_geodesic_interpolation_closure_assembly_locked():
    p = Path("docs/math/NEWSTEIN_GEODESIC_INTERPOLATION_CLOSURE_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Geodesic Interpolation Closure Assembly" in s
    assert "## Status\nOPEN" in s
    assert "the unique simple geodesic from \\(u\\) to \\(v\\) is obtained by concatenating:" in s
    assert "\\operatorname{LCA}_T(u,v)" in s
    assert "## Assembly inputs" in s
    assert "LCA interpolation closure assembly." in s
    assert "Tree geodesics coincide with unique simple paths." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{GeodesicInterpolationClosure}" in s
    assert "\\mathrm{TreePathRootedLocality}" in s
