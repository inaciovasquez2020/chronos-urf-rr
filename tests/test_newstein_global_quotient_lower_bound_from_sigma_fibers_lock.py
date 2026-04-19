from pathlib import Path

def test_newstein_global_quotient_lower_bound_from_sigma_fibers_lock() -> None:
    s = Path("docs/math/NEWSTEIN_GLOBAL_QUOTIENT_LOWER_BOUND_FROM_SIGMA_FIBERS.md").read_text()
    assert "# Newstein Global Quotient Lower Bound from Sigma Fibers" in s
    assert "Status: OPEN" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\ge 2|U|" in s
    assert "exact global lower-bound consequence extracted from the direct-sum embedding of the local sigma-fibers" in s
    assert "linearly in the number of sigma-fibers" in s
