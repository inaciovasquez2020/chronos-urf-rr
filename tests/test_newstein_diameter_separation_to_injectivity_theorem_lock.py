from pathlib import Path

def test_newstein_diameter_separation_to_injectivity_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_DIAMETER_SEPARATION_TO_INJECTIVITY_THEOREM.md").read_text()
    assert "# Newstein Diameter-Separation to Injectivity Theorem" in s
    assert "Status: OPEN" in s
    assert r"\iota_u([c_u])=\iota_v([c_v])" in s
    assert r"[c_u]=0=[c_v]" in s
    assert r"\bigoplus_{u}\bigl(Z_1(B_r(u);\mathbf F_2)/W_u\bigr)\longrightarrow Z_1/W^{\mathrm{glob}}" in s
    assert "exact theorem-level conversion from the diameter-separation obstruction to cross-fiber injectivity" in s
