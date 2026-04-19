from pathlib import Path

def test_newstein_non_factorization_from_sigma_growth_lock() -> None:
    s = Path("docs/math/NEWSTEIN_NON_FACTORIZATION_FROM_SIGMA_GROWTH.md").read_text()
    assert "# Newstein Non-Factorization from Sigma Growth" in s
    assert "Status: OPEN" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\ge 2|U|" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\to\infty" in s
    assert "cannot factor through any bounded local type space" in s
    assert "exact non-factorization consequence extracted from linear sigma-fiber growth" in s
