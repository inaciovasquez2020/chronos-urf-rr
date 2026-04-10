from pathlib import Path

def test_w5_and_growth_dependency_present():
    s = Path("docs/specs/W5_AND_GROWTH_DEPENDENCY.md").read_text()
    assert "`localTwoComplexH1Rank_growth`" in s
    assert "`W5_rank_separation`" in s
    assert "Theorem A" in s
    assert "Theorem B" in s
    assert "Theorem C" in s
    assert "Until both engines are constructive, the unconditional graph-side package is incomplete." in s
