from pathlib import Path

def test_simslv_rooted_local_exactness_closure_lock() -> None:
    s = Path("docs/math/SIMSLV_ROOTED_LOCAL_EXACTNESS_CLOSURE.md").read_text()
    assert "# SiMSLV Rooted-Local Exactness Closure" in s
    assert "Status: PROVED" in s
    assert "Status: OPEN" in s
    assert r"\partial[u,v,w]+\partial[u,v,P(w)]+\partial[u,w,P(w)]+\partial[v,w,P(w)]=0" in s
    assert r"\phi_H\!\mid_{Z_1(B_r(x))}=0" in s
