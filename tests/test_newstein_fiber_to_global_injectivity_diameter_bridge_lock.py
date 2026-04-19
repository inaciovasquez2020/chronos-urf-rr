from pathlib import Path

def test_newstein_fiber_to_global_injectivity_diameter_bridge_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY_DIAMETER_BRIDGE.md").read_text()
    assert "# Newstein Fiber-to-Global Injectivity Diameter Bridge" in s
    assert "Status: OPEN" in s
    assert r"\operatorname{diam}(\operatorname{supp} S)>L" in s
    assert r"\iota_u([c_u])=\iota_v([c_v])" in s
    assert "direct-sum embedding bridge extracted from the diameter obstruction" in s
    assert r"\bigoplus_{u} \bigl(Z_1(B_r(u))/W_u\bigr)\longrightarrow Z_1/W^{\mathrm{glob}}" in s
