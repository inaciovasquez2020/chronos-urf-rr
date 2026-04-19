from pathlib import Path

def test_newstein_fiber_to_global_injectivity_lock() -> None:
    s = Path("docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY.md").read_text()
    assert "Status: OPEN" in s
    assert r"\iota_v^{\mathrm{triv}}" in s
    assert r"\iota_v^{\mathrm{tw}}" in s
    assert r"Q(G):=" in s
    assert r"\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0" in s
    assert r"\bigoplus_v Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}" in s
    assert "No local-ball relation kills a nonzero fiber quotient class." in s
    assert "Connector edges do not create quotient identifications between different fibers." in s
    assert "Direct-sum embedding follows from fiberwise injectivity and cross-fiber independence." in s
