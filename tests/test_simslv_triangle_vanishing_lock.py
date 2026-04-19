from pathlib import Path

def test_simslv_triangle_vanishing_lock() -> None:
    s = Path("docs/math/SIMSLV_TRIANGLE_VANISHING.md").read_text()
    assert "# SiMSLV Triangle Vanishing" in s
    assert "Status: OPEN" in s
    assert r"\phi_H(\partial\tau)=0" in s
    assert r"\Phi_2(u,v,w)" in s
