from pathlib import Path

def test_newstein_assembly_theorem_lock():
    s = Path("docs/math/NEWSTEIN_ASSEMBLY_THEOREM.md").read_text()
    assert "# Newstein Assembly Theorem" in s
    assert "## Status\nOPEN" in s
    assert "theorem-level closure" in s
