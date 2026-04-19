from pathlib import Path

def test_newstein_non_factorization_theorem_lock() -> None:
    s = Path("docs/math/NEWSTEIN_NON_FACTORIZATION_THEOREM.md").read_text()
    assert "# Newstein Non-Factorization Theorem" in s
    assert "Status: OPEN" in s
    assert "does not factor through rooted radius-\\(r\\) type or \\(FO^k_r\\)-type" in s
