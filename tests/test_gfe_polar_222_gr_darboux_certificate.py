import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools/gfe/verify_gfe_polar_222_gr_darboux.py"
CERTIFICATE = ROOT / "artifacts/chronos/gfe_polar_222_gr_darboux_certificate.json"

def test_polar_222_gr_darboux_transfer() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)], cwd=ROOT, check=True,
        capture_output=True, text=True, timeout=60,
    )
    out = completed.stdout
    assert "RESULT := CERTIFIED_POLAR_222_GR_ROOT_TRANSFER" in out
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    root = record["polar_root_at_epsilon_0"]
    assert root["unique_simple_root"] is True
    assert root["multiplicity_preserved"] is True
    assert root["endpoint_conditions_preserved"] is True
    assert root["same_disk_as_axial"] is True
    assert root["disk_radius"] == 2e-5
    assert root["distance_to_plus_i_sigma_lower"] > 2.49
    assert root["distance_to_minus_i_sigma_lower"] > 1.55
    assert root["inverse_multiplier_abs_lower"] > 3.87

def test_polar_222_boundary_remains_gr_only() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["scope"]["beta2_polar_correction"] is False
    boundary = "\n".join(record["claim_boundary"]).lower()
    assert "polar root continuation" in boundary
    assert "axial-polar splitting" in boundary
    assert "unreduced trace-log" in boundary
