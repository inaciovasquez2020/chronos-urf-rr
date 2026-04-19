from pathlib import Path

def test_newstein_long_chord_exclusion_proof_surface_lock() -> None:
    s = Path("docs/math/NEWSTEIN_LONG_CHORD_EXCLUSION_PROOF_SURFACE.md").read_text()
    assert "# Newstein Long-Chord Exclusion Proof Surface" in s
    assert "Status: OPEN" in s
    assert r"\sigma_i=e_i+P_T(e_i)" in s
    assert r"e_i\notin \operatorname{supp}(w)" in s
    assert "exact theorem-level proof surface for the sigma-package exclusion step" in s
