from pathlib import Path

def test_newstein_assembly_theorem_lock():
    s = Path("docs/math/NEWSTEIN_ASSEMBLY_THEOREM.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "local coboundary criterion" in s
    assert "fiber-to-global injection lemma" in s
    assert "exact rank" in s
    assert "quotient-gap closure" in s
