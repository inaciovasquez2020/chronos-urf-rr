from pathlib import Path

def test_newstein_rooted_ball_trivialization_status_lock():
    text = Path("docs/status/NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_STATUS.md").read_text(encoding="utf-8")
    assert "\\text{Status}=\\text{OPEN-FRONTIER}." in text
    assert "NEWSTEIN_SIMPLICIAL_MULTI_PARENT_REPLACEMENT_LEMMA.md" in text
    assert "No unconditional proof closure is claimed in the repository." in text
    assert "All downstream steps reduce to the multi-parent replacement lemma" in text
