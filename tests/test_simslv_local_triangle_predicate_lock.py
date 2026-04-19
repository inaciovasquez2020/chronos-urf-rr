from pathlib import Path

def test_simslv_local_triangle_predicate_lock() -> None:
    s = Path("docs/math/SIMSLV_LOCAL_TRIANGLE_PREDICATE.md").read_text()
    assert "# SiMSLV Local Triangle Predicate" in s
    assert "Status: OPEN" in s
    assert r"\Phi_2(u,v,w)" in s
    assert "Finish condition" in s
