from pathlib import Path
import json
import yaml

def test_petersen_2lift_artifact_exists_and_matches():
    p = Path("artifacts/petersen_2lift_urf_witness_r2.json")
    assert p.exists()
    data = json.loads(p.read_text())

    assert data["base_graph"] == "Petersen"
    assert data["radius"] == 2
    assert data["cutoff"] == 5

    assert data["G_plus"]["z1_dimension"] == 12
    assert data["G_plus"]["local_cycle_span_dimension"] == 12
    assert data["G_plus"]["urf_invariant"] == 0

    assert data["G_minus"]["z1_dimension"] == 11
    assert data["G_minus"]["local_cycle_span_dimension"] == 10
    assert data["G_minus"]["urf_invariant"] == 1

def test_witness_status_partial_compute():
    p = Path("witness_instance/WITNESS_INSTANCE_STATUS.yaml")
    assert p.exists()
    data = yaml.safe_load(p.read_text())

    assert data["status"] == "partial_compute"
    assert data["base_graph_fixed"] is True
    assert data["lift_defined"] is True
    assert data["local_property_checked"] is False
    assert data["invariant_computed"] is True
    assert data["separation_verified"] is True
    assert data["G_plus_urf_invariant"] == 0
    assert data["G_minus_urf_invariant"] == 1
