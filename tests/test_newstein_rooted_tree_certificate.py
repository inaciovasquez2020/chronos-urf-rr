from pathlib import Path

def test_newstein_rooted_tree_certificate_lock():
    s = Path("docs/math/NEWSTEIN_ROOTED_TREE_CERTIFICATE.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in s
    assert "strict descent operator" in s
    assert "d(r,v)" in s
    assert "local coboundary criterion" in s
