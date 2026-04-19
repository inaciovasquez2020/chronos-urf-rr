from pathlib import Path

def test_simslv_ball_simple_connectedness_lock() -> None:
    s = Path("docs/math/SIMSLV_BALL_SIMPLE_CONNECTEDNESS.md").read_text()
    assert "# SiMSLV Ball Simple Connectedness" in s
    assert "Status: OPEN" in s
    assert r"L>2r+1" in s
    assert r"\operatorname{girth}(X_n)>2r+1" in s
