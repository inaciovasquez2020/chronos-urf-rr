from pathlib import Path

def test_newstein_fiber_quotient_rank_computation_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_COMPUTATION_THEOREM.md").read_text()
    assert "# Newstein Fiber Quotient Rank Computation Theorem" in s
    assert "Status: OPEN" in s
    assert "=4" in s
    assert "=2" in s
