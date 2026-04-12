from pathlib import Path

def test_newstein_20_percent_coverage_plan_lock():
    s = Path("docs/status/NEWSTEIN_20_PERCENT_COVERAGE_PLAN.md").read_text()
    assert "# Newstein 20 Percent Coverage Plan" in s
    assert "does not prove a literal 20% mathematical increase" in s
    assert "Coverage is structural, not theorem-level closure." in s
