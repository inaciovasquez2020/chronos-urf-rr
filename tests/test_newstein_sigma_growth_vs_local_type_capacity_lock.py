from pathlib import Path

def test_newstein_sigma_growth_vs_local_type_capacity_lock() -> None:
    s = Path("docs/math/NEWSTEIN_SIGMA_GROWTH_VS_LOCAL_TYPE_CAPACITY.md").read_text()
    assert "# Newstein Sigma Growth vs Local-Type Capacity" in s
    assert "Status: OPEN" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\to\infty" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\le C(r,k,\Delta)" in s
    assert "exact contradiction surface between unbounded sigma-growth and bounded local-type capacity" in s
    assert "bounded local-type factorization fails" in s
