from pathlib import Path

def test_newstein_local_acyclicity_lock():
    s = Path("docs/math/NEWSTEIN_LOCAL_ACYCLICITY.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "H_1" in s
    assert "strict parent descent" in s
    assert "local coboundary criterion" in s
