from pathlib import Path

def test_blockers_and_next_actions_present():
    s = Path("docs/status/BLOCKERS_AND_NEXT_ACTIONS.md").read_text()
    assert "localTwoComplexH1Rank_growth" in s
    assert "W5_rank_separation" in s
    assert "Immediate executable actions" in s
    assert "Closure condition" in s
