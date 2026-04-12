from pathlib import Path

def test_newstein_parent_depth_decrement_assembly_locked():
    p = Path("docs/math/NEWSTEIN_PARENT_DEPTH_DECREMENT_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Parent-Depth Decrement Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T(v))=\\operatorname{depth}_T(v)-1" in s
    assert "## Assembly inputs" in s
    assert "Parent-depth length identity sublemma." in s
    assert "\\operatorname{depth}_T(x)=d_T(r,x)." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{ParentDepthDecrement\\ assembly}" in s
    assert "\\mathrm{RootedDistanceMonotonicity}" in s
