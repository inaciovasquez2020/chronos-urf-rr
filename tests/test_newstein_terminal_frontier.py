from pathlib import Path

def test_newstein_terminal_frontier_lock():
    s = Path("docs/status/NEWSTEIN_TERMINAL_FRONTIER.md").read_text()
    assert "# Newstein Terminal Frontier" in s
    assert "## Status\nOPEN" in s
    assert "NEWSTEIN_FUNDAMENTAL_CYCLE_GENERATION_SUBLEMMA.md" in s
    assert "NEWSTEIN_ASSEMBLY_THEOREM.md" in s
