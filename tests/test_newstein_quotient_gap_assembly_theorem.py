from pathlib import Path

def test_newstein_quotient_gap_assembly_theorem_locked():
    p = Path("docs/math/NEWSTEIN_QUOTIENT_GAP_ASSEMBLY_THEOREM.md")
    s = p.read_text()
    assert "# Newstein Quotient-Gap Assembly Theorem" in s
    assert "## Status\nCONDITIONAL" in s
    assert "Consequently, the quotient-gap assembly closes conditionally from the locked dependency chain." in s
    assert "## Dependency chain" in s
    assert "\\mathrm{QuotientGapAssemblyTheorem}" in s
    assert "## Frontier status" in s
    assert "This closes the assembly layer only." in s
    assert "The theorem-level closure remains conditional until the locked assembly inputs are replaced by verified theorem proofs." in s
    assert "## Canonical remaining theorem-level obligations" in s
    assert "Verify the parent-depth decrement theorem." in s
    assert "Verify the rooted-ball trivialization theorem." in s
    assert "Verify the fiber quotient-rank computation." in s
    assert "Verify direct-sum independence at theorem level." in s
    assert "Verify the per-step information bound at theorem level." in s
