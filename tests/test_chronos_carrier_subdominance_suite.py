import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALL_ART = ROOT / "artifacts/chronos/all_registered_carrier_subdominance.json"
LEMMA_ART = ROOT / "artifacts/chronos/simulator_to_universal_carrier_lemma.json"

def test_all_registered_simulator_carriers_generate():
    subprocess.run(["python3", "tools/simulate_all_registered_carriers.py"], cwd=ROOT, check=True)
    data = json.loads(ALL_ART.read_text())
    assert data["status"] == "ALL_REGISTERED_CARRIERS_SIMULATED_ONLY"
    assert data["theorem_closure"] is False
    assert data["uniform_carrier_subdominance_proved"] is False
    assert data["registered_admissible_carriers_all_pass"] is True

def test_all_registered_admissible_carriers_eventually_subdominant():
    data = json.loads(ALL_ART.read_text())
    for carrier in data["carrier_results"]:
        if not carrier["admissible"]:
            continue
        start = carrier["holds_from_lambda"]
        assert start is not None
        for row in carrier["rows"]:
            if row["lambda"] >= start:
                assert row["transcript_capacity"] < row["obs_dim"]

def test_forbidden_oracle_carriers_are_not_admissible():
    data = json.loads(ALL_ART.read_text())
    forbidden = [c for c in data["carrier_results"] if not c["admissible"]]
    assert forbidden
    for carrier in forbidden:
        assert "obstruction-oracle" in carrier["reason_for_exclusion"]
        assert carrier["eventual_subdominance_verified_on_range"] is False

def test_all_registered_verifier_preserves_frontier_boundary():
    subprocess.run(["python3", "tools/verify_all_registered_carrier_subdominance.py"], cwd=ROOT, check=True)

def test_simulator_to_universal_carrier_artifact_boundary():
    data = json.loads(LEMMA_ART.read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["theorem_closure"] is False
    assert data["proves_chronos_rr_closure"] is False

def test_simulator_to_universal_carrier_verifier():
    subprocess.run(
        ["python3", "tools/verify_simulator_to_universal_carrier_lemma.py"],
        cwd=ROOT,
        check=True,
    )
