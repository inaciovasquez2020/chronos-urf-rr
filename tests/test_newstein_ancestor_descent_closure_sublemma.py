from pathlib import Path

def test_newstein_ancestor_descent_closure_sublemma_lock():
    s = Path("docs/math/NEWSTEIN_ANCESTOR_DESCENT_CLOSURE_SUBLEMMA.md").read_text()
    assert "# Newstein Ancestor-Descent Closure Sublemma" in s
    assert "## Status\nOPEN" in s
    assert "stable under parent iteration" in s
