import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_normal_form.json"

def test_carrier_registry_exhaustiveness_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["theorem_closure"] is False
    assert data["uniform_carrier_subdominance_proved"] is False
    assert data["proves_chronos_rr_closure"] is False

def test_registered_classes_exclude_oracle_boundaries():
    data = json.loads(ART.read_text())
    registered = set(data["registered_subdominant_classes"])
    forbidden = set(data["forbidden_boundary_classes"])
    assert "obstruction_oracle_capacity" not in registered
    assert "obstruction_plus_one_capacity" not in registered
    assert "obstruction_oracle_capacity" in forbidden
    assert "obstruction_plus_one_capacity" in forbidden

def test_carrier_registry_exhaustiveness_verifier():
    subprocess.run(
        ["python3", "tools/verify_carrier_registry_exhaustiveness_normal_form.py"],
        cwd=ROOT,
        check=True,
    )
