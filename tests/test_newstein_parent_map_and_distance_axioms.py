from pathlib import Path

def test_newstein_parent_map_and_distance_axioms_lock() -> None:
    text = Path("docs/math/NEWSTEIN_PARENT_MAP_AND_DISTANCE_AXIOMS.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "\\eta : B_R(r) \\to B_R(r)." in text
    assert "\\eta(r)=r." in text
    assert "(\\eta(w),w)\\in E." in text
    assert "d(\\,\\cdot\\,,r): B_R(r)\\to \\mathbf N." in text
    assert "d(r,r)=0." in text
    assert "\\eta(w)\\) lies on a shortest path from \\(w\\) to \\(r\\)" in text
    assert "d(u,r)\\le d(v,r)+1" in text
    assert "d(v,r)\\le d(u,r)+1" in text
    assert "w \\neq r \\Longrightarrow d(\\eta(w),r)=d(w,r)-1" in text
