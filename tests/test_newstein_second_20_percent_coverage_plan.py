from pathlib import Path

def test_newstein_second_20_percent_coverage_plan_lock():
    s = Path("docs/status/NEWSTEIN_SECOND_20_PERCENT_COVERAGE_PLAN.md").read_text()
    assert "# Newstein Second 20 Percent Coverage Plan" in s
    assert "Coverage is structural, not theorem-level closure." in s
