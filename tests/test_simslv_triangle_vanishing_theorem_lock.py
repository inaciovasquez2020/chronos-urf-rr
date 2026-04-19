from pathlib import Path

def test_simslv_triangle_vanishing_theorem_lock() -> None:
    s = Path("docs/math/SIMSLV_TRIANGLE_VANISHING_THEOREM.md").read_text()
    assert "# SiMSLV Triangle Vanishing Theorem" in s
    assert "Status: OPEN" in s
    assert r"\phi_H(\partial\tau)=0" in s
    assert "case split" in s
