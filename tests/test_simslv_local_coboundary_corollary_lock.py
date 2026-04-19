from pathlib import Path

def test_simslv_local_coboundary_corollary_lock() -> None:
    s = Path("docs/math/SIMSLV_LOCAL_COBOUNDARY_COROLLARY.md").read_text()
    assert "# SiMSLV Local Coboundary Corollary" in s
    assert "Status: OPEN" in s
    assert r"\phi_H\!\mid_{Z_1(B_r(x))}=0" in s
    assert "twisted/trivial witness structures" in s
