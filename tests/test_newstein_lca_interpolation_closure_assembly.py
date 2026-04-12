from pathlib import Path

def test_newstein_lca_interpolation_closure_assembly_locked():
    p = Path("docs/math/NEWSTEIN_LCA_INTERPOLATION_CLOSURE_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein LCA Interpolation Closure Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{par}_T^{\\,m_\\ast}(u)=\\operatorname{par}_T^{\\,m_\\ast}(v)" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T^{\\,m}(u))" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T^{\\,m}(v))" in s
    assert "## Assembly inputs" in s
    assert "Ancestor descent closure assembly." in s
    assert "lowest common ancestors in rooted trees" in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{LCAInterpolationClosure}" in s
    assert "\\mathrm{GeodesicInterpolationClosure}" in s
