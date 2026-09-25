import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools/gfe/verify_gfe_axial_221_epsilon_continuation.py"
CERTIFICATE = ROOT / "artifacts/chronos/gfe_axial_221_epsilon_continuation_certificate.json"


def _receipt_value(output: str, key: str) -> str:
    prefix = key + " := "
    for line in output.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise AssertionError(f"missing receipt key: {key}")


def test_gfe_axial_221_epsilon_continuation_certificate() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    output = completed.stdout
    assert "RESULT := CERTIFIED_UNIFORM_UNIQUE_SIMPLE_ROOT_TUBE" in output

    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["schema"] == (
        "chronos.gfe_axial_221_epsilon_continuation_certificate.v1"
    )
    assert record["scope"]["epsilon_interval"] == [0.0, 0.0001]
    assert record["scope"]["overtone"] == 1

    tube = record["root_tube"]
    assert tube["unique_zero_counting_multiplicity_for_each_epsilon"] == 1
    assert tube["simple_root_for_each_epsilon"] is True
    assert tube["uniform_disk_radius"] == 5e-6

    gates = record["gates"]
    assert gates["horizon_majorant_lt_one"] is True
    assert gates["infinity_damping_positive"] is True
    assert gates["rouche_margin_positive"] is True
    assert gates["rouche_linear_lower"] > gates["rouche_error_upper"]

    assert abs(
        float(_receipt_value(output, "HORIZON_MAJORANT_Q"))
        - gates["horizon_majorant_q_upper"]
    ) < 1e-15
    assert abs(
        float(_receipt_value(output, "INFINITY_DAMPING_LOWER"))
        - gates["infinity_damping_lower"]
    ) < 1e-15
    assert abs(
        float(_receipt_value(output, "ROUCHE_MARGIN"))
        - gates["rouche_margin_lower"]
    ) < 1e-15


def test_claim_boundary_keeps_stronger_claims_open() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    boundary = "\n".join(record["claim_boundary"]).lower()
    assert "domega_221/depsilon" in boundary
    assert "polar sector" in boundary
    assert "unreduced trace-log" in boundary
    assert "full gravity closure" in boundary
