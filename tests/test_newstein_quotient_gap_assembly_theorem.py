from pathlib import Path


def test_newstein_quotient_gap_assembly_theorem_locked():
    s = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_ASSEMBLY_THEOREM.md").read_text()
    assert "# Newstein Quotient-Gap Assembly Theorem" in s
    assert "Status: PROVED" in s
    assert "global quotient-gap lower bound" in s
    assert "surviving fiber quotient has rank 4 over F_2" in s
    assert "injects into the global quotient" in s
    assert "leaks at most V_C information" in s
