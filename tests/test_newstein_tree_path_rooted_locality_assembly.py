from pathlib import Path

def test_newstein_tree_path_rooted_locality_assembly_locked():
    p = Path("docs/math/NEWSTEIN_TREE_PATH_ROOTED_LOCALITY_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Tree-Path Rooted Locality Assembly" in s
    assert "## Status\nOPEN" in s
    assert "the unique geodesic from \\(u\\) to \\(v\\) is completely determined by rooted ancestor data" in s
    assert "\\operatorname{LCA}_T(u,v)" in s
    assert "the \\(u\\)-to-\\(v\\) tree path is rooted-local" in s
    assert "## Assembly inputs" in s
    assert "Geodesic interpolation closure assembly." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{TreePathRootedLocality}" in s
    assert "\\mathrm{FundamentalCycleGeneration}" in s
