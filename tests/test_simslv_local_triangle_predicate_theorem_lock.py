from pathlib import Path

def test_simslv_local_triangle_predicate_theorem_lock() -> None:
    s = Path("docs/math/SIMSLV_LOCAL_TRIANGLE_PREDICATE_THEOREM.md").read_text()
    assert "# SiMSLV Local Triangle Predicate Theorem" in s
    assert "Status: OPEN" in s
    assert r"\Phi_2(u,v,w)" in s
    assert "substitution-stability proof" in s
