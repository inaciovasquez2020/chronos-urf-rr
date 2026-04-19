from pathlib import Path

def test_newstein_per_step_information_bound_lock() -> None:
    s = Path("docs/math/NEWSTEIN_PER_STEP_INFORMATION_BOUND.md").read_text()
    assert "Status: OPEN" in s
    assert r"\Delta I_t \le C" in s
    assert "Explicit admissible refinement model." in s
    assert "Definition of one-step transcript/information increment." in s
    assert "Uniform constant-capacity bound per admissible step." in s
    assert "Independence of the bound from \\(n\\)." in s
    assert "Compatibility with the quotient-gap assembly." in s
    assert r"T_n \ge \frac{2|V(X_n)|}{C}" in s
    assert r"T_n=\Omega(n)." in s
