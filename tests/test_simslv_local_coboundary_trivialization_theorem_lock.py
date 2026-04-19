from pathlib import Path

def test_simslv_local_coboundary_trivialization_theorem_lock() -> None:
    s = Path("docs/math/SIMSLV_LOCAL_COBOUNDARY_TRIVIALIZATION_THEOREM.md").read_text()
    assert "# SiMSLV Local Coboundary Trivialization Theorem" in s
    assert "Status: OPEN" in s
    assert r"\phi_H\!\mid_{Z_1(B_r(x))}=0" in s
    assert "rooted-ball trivialization" in s
