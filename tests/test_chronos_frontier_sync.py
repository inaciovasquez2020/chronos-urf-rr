from pathlib import Path

def test_chronos_frontier_sync():
    s = Path("docs/status/WHOLE_URF_FRONTIER_POINTER.md").read_text()
    assert "URF_REMAINING_FRONTIER_CANONICAL.md" in s
    assert "Canonical pointer" in s
