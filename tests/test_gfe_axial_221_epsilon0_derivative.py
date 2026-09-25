import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools/gfe/verify_gfe_axial_221_epsilon0_derivative.py"
CERTIFICATE = ROOT / "artifacts/chronos/gfe_axial_221_epsilon0_derivative_certificate.json"

def value(output: str, key: str) -> float:
    prefix = key + " := "
    for line in output.splitlines():
        if line.startswith(prefix):
            return float(line[len(prefix):])
    raise AssertionError(f"missing receipt key: {key}")

def test_axial_221_epsilon0_implicit_derivative() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT, check=True, capture_output=True, text=True, timeout=180,
    )
    out = completed.stdout
    assert "RESULT := CERTIFIED_EPSILON0_IMPLICIT_DERIVATIVE" in out
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    d = record["implicit_derivative"]
    assert d["D_Omega_nonzero"] is True
    assert d["real_part_positive"] is True
    assert d["imag_part_negative"] is True
    assert value(out, "ROOT_RADIUS") == 1.1e-6
    assert abs(value(out, "DERIVATIVE_RADIUS") - d["disk_radius"]) < 1e-12
    assert value(out, "DERIVATIVE_REAL_LOWER") > 0
    assert value(out, "DERIVATIVE_IMAG_UPPER") < 0

def test_derivative_boundary_remains_bounded() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    boundary = "\n".join(record["claim_boundary"]).lower()
    assert "polar derivative" in boundary
    assert "unreduced trace-log" in boundary
    assert "full gravity closure" in boundary
