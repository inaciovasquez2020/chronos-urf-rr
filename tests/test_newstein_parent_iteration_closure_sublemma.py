from pathlib import Path

def test_newstein_parent_iteration_closure_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_PARENT_ITERATION_CLOSURE_SUBLEMMA.md").read_text()
    assert "# Newstein Parent-Iteration Closure Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "\\operatorname{par}_T(w)\\in B_R(v)" in s
