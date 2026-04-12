from pathlib import Path

def test_newstein_function_completion_frontier_lock():
    s = Path("docs/status/NEWSTEIN_FUNCTION_COMPLETION_FRONTIER.md").read_text()
    assert "# Newstein Function Completion Frontier" in s
    assert "## Status\nOPEN" in s
    for name in [
        "NEWSTEIN_LOCAL_COBOUNDARY_CRITERION.md",
        "NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_LEMMA.md",
        "NEWSTEIN_FIBER_QUOTIENT_RANK_LEMMA.md",
        "NEWSTEIN_DIRECT_SUM_INDEPENDENCE_LEMMA.md",
        "NEWSTEIN_FIBER_TO_GLOBAL_INJECTION_LEMMA.md",
        "NEWSTEIN_PER_STEP_INFORMATION_BOUND.md",
        "NEWSTEIN_ASSEMBLY_THEOREM.md",
    ]:
        assert name in s
