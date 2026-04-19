from pathlib import Path

def test_newstein_per_step_information_bound_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND_THEOREM.md").read_text()
    assert "# Newstein Per-Step Information Bound Theorem" in s
    assert "Status: OPEN" in s
    assert r"\Delta I_t \le C" in s
    assert r"T_n \ge \frac{2|V(X_n)|}{C}" in s
