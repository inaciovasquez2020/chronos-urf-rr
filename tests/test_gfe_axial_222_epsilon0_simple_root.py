import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools/gfe/verify_gfe_axial_222_epsilon0_simple_root.py"
CERTIFICATE = ROOT / "artifacts/chronos/gfe_axial_222_epsilon0_simple_root_certificate.json"

def value(output: str, key: str) -> float:
    prefix = key + " := "
    for line in output.splitlines():
        if line.startswith(prefix):
            return float(line[len(prefix):])
    raise AssertionError(f"missing receipt key: {key}")

def test_axial_222_epsilon0_simple_root() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT, check=True, capture_output=True, text=True, timeout=180,
    )
    out = completed.stdout
    assert "GFE_AXIAL_222_EPSILON0_FAST_AFFINE" in out
    assert "RESULT := CERTIFIED_UNIQUE_SIMPLE_ROOT_DISK" in out
    assert value(out, "OMEGA_RADIUS") == 2e-5
    assert value(out, "HORIZON_MAJORANT_Q") < 1
    assert value(out, "INFINITY_DAMPING_LOWER") > 0
    assert value(out, "ROUCHE_MARGIN") > 0
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["schema"] == "chronos.gfe_axial_222_epsilon0_simple_root_certificate.v1"
    assert record["root_disk"]["radius"] == 2e-5
    assert record["root_disk"]["unique_zero_counting_multiplicity"] == 1
    assert record["root_disk"]["simple_root"] is True
    assert all(record["verified_gates"].values())

def test_axial_222_boundary_remains_bounded() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    boundary = "\n".join(record["claim_boundary"]).lower()
    assert "epsilon>0 continuation" in boundary
    assert "polar sector" in boundary
    assert "unreduced trace-log" in boundary
    assert "full gravity closure" in boundary
