from pathlib import Path

def test_newstein_diameter_separation_filling_obstruction_lock() -> None:
    s = Path("docs/math/NEWSTEIN_DIAMETER_SEPARATION_FILLING_OBSTRUCTION.md").read_text()
    assert "# Newstein Diameter-Separation Filling Obstruction" in s
    assert "Status: OPEN" in s
    assert r"[c_u]\in Z_1(B_r(u);\mathbf F_2)/W_u" in s
    assert r"[c_v]\in Z_1(B_r(v);\mathbf F_2)/W_v" in s
    assert r"\partial S=c_u-c_v" in s
    assert r"\operatorname{diam}(\operatorname{supp} S)>L" in s
    assert "weakest theorem-level obstruction still needed" in s
