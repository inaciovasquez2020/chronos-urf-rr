from pathlib import Path

def test_newstein_fundamental_cycle_generation_sublemma_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md").read_text()
    assert "# Newstein Fundamental Cycle Generation Sublemma" in s
    assert "Status: OPEN" in s
    assert r"Z_1(B_r(x);\mathbb F_2)" in s
    assert r"\Phi_2(u,v,w)" in s
    assert "weakest named missing object" in s
