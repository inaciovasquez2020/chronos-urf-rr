from pathlib import Path

def test_newstein_local_type_capacity_bound_surface_lock() -> None:
    s = Path("docs/math/NEWSTEIN_LOCAL_TYPE_CAPACITY_BOUND_SURFACE.md").read_text()
    assert "# Newstein Local-Type Capacity Bound Surface" in s
    assert "Status: OPEN" in s
    assert r"Q\) factors through a bounded local type space depending only on \((r,k,\Delta)\)" in s
    assert r"\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\le C(r,k,\Delta)" in s
    assert "exact theorem-level proof surface for the bounded-capacity half of the final contradiction" in s
