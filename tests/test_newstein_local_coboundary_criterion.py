from pathlib import Path

def test_newstein_local_coboundary_criterion_lock():
    s = Path("docs/math/NEWSTEIN_LOCAL_COBOUNDARY_CRITERION.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "H_1" in s
    assert "local boundary" in s
    assert "fiber-to-global injection" in s
