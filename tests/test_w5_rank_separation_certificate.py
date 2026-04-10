import json
from pathlib import Path

def test_w5_rank_separation_certificate() -> None:
    d = json.loads(Path("URF/Witnesses/W5_CERTIFICATE.json").read_text())
    assert d["name"] == "W(5)_2_lift_rank_separation"
    assert d["R"] == 3
    assert d["degree"] == 6
    assert d["girth"] == 8
    assert d["vertices_base"] == 312
    assert d["edges_base"] == 936
    assert d["vertices_lift"] == 624
    assert d["edges_lift"] == 1872
    assert d["Z1dim_G_plus"] == 1250
    assert d["Z1dim_G_minus"] == 1249
    assert d["quotient_difference"] == 1
    assert d["local_cycle_bound"] == 7
    assert d["local_trivial"] is True
    assert d["FOkR_equivalent"] is True
    assert d["status"] == "CERTIFIED"
