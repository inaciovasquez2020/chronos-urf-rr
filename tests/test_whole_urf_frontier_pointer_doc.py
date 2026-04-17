from pathlib import Path

def test_whole_urf_frontier_pointer_doc():
    s = Path("docs/status/WHOLE_URF_FRONTIER_POINTER.md").read_text()
    assert "This repository does not define whole-URF residual frontier status." in s
    assert "Canonical whole-URF residual frontier:" in s
    assert "URF_REMAINING_FRONTIER_CANONICAL.md" in s
    assert "must not escalate whole-URF status" in s
