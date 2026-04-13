from pathlib import Path

def test_newstein_geodesic_parent_law_lock() -> None:
    text = Path("docs/math/NEWSTEIN_GEODESIC_PARENT_LAW.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "w \\neq r" in text
    assert "\\eta(w)\\) lies on a shortest path from \\(w\\) to \\(r\\)" in text
    assert "d(w,r)=1+d(\\eta(w),r)." in text
    assert "weakest sufficient remaining ingredient for the one-step parent-depth decrement proof shell" in text
