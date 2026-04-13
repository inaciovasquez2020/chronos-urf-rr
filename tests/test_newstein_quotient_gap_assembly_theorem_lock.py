from pathlib import Path


def test_newstein_quotient_gap_assembly_theorem_lock():
    text = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_ASSEMBLY_THEOREM.md").read_text()
    assert "Status: PROVED" in text
    assert "global quotient-gap lower bound" in text
    assert "surviving fiber quotient has rank 4 over F_2" in text
    assert "injects into the global quotient" in text
    assert "leaks at most V_C information" in text
    assert "Quotient-Gap Assembly Theorem" in text
