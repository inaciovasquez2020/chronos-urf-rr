from pathlib import Path

def test_newstein_final_non_factorization_assembly_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FINAL_NON_FACTORIZATION_ASSEMBLY.md").read_text()
    assert "# Newstein Final Non-Factorization Assembly" in s
    assert "Status: OPEN" in s
    assert "terminal assembly surface for the Newstein non-factorization conclusion" in s
    assert "does not factor through rooted radius-" in s
    assert "does not factor through } FO^k_r" in s or "does not factor through } FO^k_r\\text{-type}" in s or "does not factor through } FO^k_r" in s
