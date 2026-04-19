from pathlib import Path

def test_newstein_closure_set_lock() -> None:
    s = Path("docs/status/NEWSTEIN_CLOSURE_SET.md").read_text()
    assert "Status: OPEN" in s
    assert "docs/math/NEWSTEIN_LOCAL_TRIANGLE_GENERATION_THEOREM.md" in s
    assert "docs/math/NEWSTEIN_TRIANGLE_VANISHING_THEOREM.md" in s
    assert "docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_COMPUTATION.md" in s
    assert "docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY.md" in s
    assert "docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND.md" in s
    assert "docs/math/NEWSTEIN_QUOTIENT_GAP_THEOREM.md" in s
    assert "docs/math/NEWSTEIN_NON_FACTORIZATION_CONSEQUENCE.md" in s
    assert "reduction-complete and theorem-incomplete" in s
