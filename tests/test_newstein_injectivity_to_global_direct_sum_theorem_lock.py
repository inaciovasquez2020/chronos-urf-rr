from pathlib import Path

def test_newstein_injectivity_to_global_direct_sum_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_INJECTIVITY_TO_GLOBAL_DIRECT_SUM_THEOREM.md").read_text()
    assert "# Newstein Injectivity-to-Global Direct-Sum Theorem" in s
    assert "Status: OPEN" in s
    assert r"V_u\subseteq Z_1(B_r(u);\mathbf F_2)/W_u" in s
    assert r"\bigoplus_{u\in U} V_u \longrightarrow Z_1/W^{\mathrm{glob}}" in s
    assert "global quotient contains the direct sum of the local sigma-fiber twisted subspaces" in s
    assert "exact theorem-level step upgrading cross-fiber injectivity into a genuine global direct-sum embedding" in s
