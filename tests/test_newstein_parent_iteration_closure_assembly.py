from pathlib import Path

def test_newstein_parent_iteration_closure_assembly_locked():
    p = Path("docs/math/NEWSTEIN_PARENT_ITERATION_CLOSURE_ASSEMBLY.md")
    s = p.read_text()
    assert "# Newstein Parent Iteration Closure Assembly" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T^{\\,m}(u))" in s
    assert "\\operatorname{depth}_T(\\operatorname{par}_T^{\\,m}(v))" in s
    assert "## Assembly inputs" in s
    assert "One-step parent stability assembly." in s
    assert "Parent-depth decrement assembly." in s
    assert "## Proof skeleton" in s
    assert "\\mathrm{ParentIterationClosure}" in s
    assert "\\mathrm{AncestorDescentClosure}" in s
