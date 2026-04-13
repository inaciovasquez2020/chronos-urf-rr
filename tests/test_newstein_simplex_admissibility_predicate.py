from pathlib import Path

def test_newstein_simplex_admissibility_predicate_lock():
    text = Path("docs/math/NEWSTEIN_SIMPLEX_ADMISSIBILITY_PREDICATE.md").read_text(encoding="utf-8")
    assert "\\mathrm{Simp}_m(x_0,\\dots,x_m)" in text
    assert "\\mathrm{Simp}_m(y_0,\\dots,y_m)" in text
    assert "\\text{OPEN}." in text
    assert "No unconditional defining formula for }\\mathrm{Simp}_m" in text

def test_newstein_multi_parent_replacement_proof_target_lock():
    text = Path("docs/math/NEWSTEIN_MULTI_PARENT_REPLACEMENT_PROOF_TARGET.md").read_text(encoding="utf-8")
    assert "\\forall I\\subseteq\\{0,\\dots,m\\}" in text
    assert "\\text{OPEN-FRONTIER}." in text
    assert "\\text{No theorem-level promotion is licensed.}" in text
