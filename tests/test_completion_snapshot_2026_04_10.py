from pathlib import Path

def test_completion_snapshot_present():
    s = Path("docs/status/COMPLETION_SNAPSHOT_2026_04_10.md").read_text()
    assert "68\\% \\text{ complete for the unconditional graph-side package}" in s
    assert "45\\% \\text{ overall}" in s
    assert "localTwoComplexH1Rank_growth" in s
    assert "W5_rank_separation" in s
    assert "formal definition of `ED(P_n)`" in s
