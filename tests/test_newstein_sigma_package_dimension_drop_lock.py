from pathlib import Path

def test_newstein_sigma_package_dimension_drop_lock() -> None:
    s = Path("docs/math/NEWSTEIN_SIGMA_PACKAGE_DIMENSION_DROP.md").read_text()
    assert "# Newstein Sigma-Package Dimension Drop" in s
    assert "Status: OPEN" in s
    assert r"\sigma_i=e_i+P_T(e_i)" in s
    assert r"\dim_{\mathbf F_2}(W^{\mathrm{tw}}/W^{\mathrm{triv}})=2" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{tw}})=2" in s
    assert "exact rank-drop consequence of the \\(\\sigma\\)-construction" in s
