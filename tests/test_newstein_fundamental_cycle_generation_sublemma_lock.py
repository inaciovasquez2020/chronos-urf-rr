from pathlib import Path

def test_newstein_fundamental_cycle_generation_sublemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Sublemma" in s
    assert "Status: OPEN" in s
    assert "## Target statement" in s
    assert "## Exact closure target" in s
    assert "docs/math/NEWSTEIN_LOCAL_TRIANGLE_GENERATION_THEOREM.md" in s
    assert "docs/math/NEWSTEIN_TRIANGLE_VANISHING_THEOREM.md" in s
    assert "docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_COMPUTATION.md" in s
    assert "docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY.md" in s
    assert "docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND.md" in s
    assert "## Deduction target" in s
    assert "## Status" in s
    assert "weakest missing object" in s
    assert "## Finish condition" in s
