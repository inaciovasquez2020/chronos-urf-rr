from pathlib import Path

def test_newstein_ancestor_descent_closure_assembly_locked():
    p = Path("docs/math/NEWSTEIN_ANCESTOR_DESCENT_CLOSURE_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Ancestor Descent Closure Assembly" in s
    assert "## Status\nOPEN" in s
    assert "the ancestor chains of \\(u\\) and \\(v\\) descend through equal rooted depths" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T^{\\,m}(u))" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T^{\\,m}(v))" in s
    assert "## Assembly inputs" in s
    assert "Parent iteration closure assembly." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{AncestorDescentClosure}" in s
    assert "\\mathrm{LCAInterpolationClosure}" in s
