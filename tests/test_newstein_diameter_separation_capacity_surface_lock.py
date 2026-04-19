from pathlib import Path

def test_newstein_diameter_separation_capacity_surface_lock() -> None:
    s = Path("docs/math/NEWSTEIN_DIAMETER_SEPARATION_CAPACITY_SURFACE.md").read_text()
    assert "# Newstein Diameter-Separation Capacity Surface" in s
    assert "Status: OPEN" in s
    assert r"[c_u]\in Z_1(B_r(u);\mathbf F_2)/W_u" in s
    assert r"[c_v]\in Z_1(B_r(v);\mathbf F_2)/W_v" in s
    assert r"\operatorname{diam}(\operatorname{supp} S)>L" in s
    assert "exact theorem-level proof surface for the cross-fiber diameter-separation obstruction" in s
