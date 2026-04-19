from pathlib import Path

def test_newstein_local_type_capacity_contradiction_corollary_lock() -> None:
    s = Path("docs/math/NEWSTEIN_LOCAL_TYPE_CAPACITY_CONTRADICTION_COROLLARY.md").read_text()
    assert "# Newstein Local-Type Capacity Contradiction Corollary" in s
    assert "Status: OPEN" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\to\infty" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\le C(r,k,\Delta)" in s
    assert "does not factor through rooted radius-\\(r\\) type" in s
    assert "does not factor through \\(FO^k_r\\)-type" in s
