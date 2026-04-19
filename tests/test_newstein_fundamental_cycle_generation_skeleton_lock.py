from pathlib import Path

def test_newstein_fundamental_cycle_generation_skeleton_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SKELETON.md").read_text()
    assert "Status: OPEN" in s
    assert "Prove the local triangle-generation theorem for radius-" in s
    assert "Fix an explicit twisted cocycle and verify triangle-vanishing by case split on triangle types." in s
    assert r"\(Z_1(\widetilde T)/W \cong H_1(\widetilde T;\mathbb F_2)\)" in s
    assert "Prove fiber inclusion injects modulo local-ball spans." in s
    assert r"\(\Delta I_t\le C\)" in s
    assert "explicit witness pair" in s
    assert "local-type equality" in s
    assert "local-agreement" in s
    assert "global invariant-gap" in s
    assert "treewidth-divergence" in s
