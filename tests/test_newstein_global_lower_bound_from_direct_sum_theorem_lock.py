from pathlib import Path

def test_newstein_global_lower_bound_from_direct_sum_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_GLOBAL_LOWER_BOUND_FROM_DIRECT_SUM_THEOREM.md").read_text()
    assert "# Newstein Global Lower Bound from Direct-Sum Theorem" in s
    assert "Status: OPEN" in s
    assert r"V_u\subseteq Z_1(B_r(u);\mathbf F_2)/W_u" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})" in s
    assert r"2|U|" in s
    assert "exact theorem-level lower-bound extraction from the global direct-sum embedding of the local sigma-fiber subspaces" in s
