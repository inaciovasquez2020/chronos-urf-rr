import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools/gfe/verify_gfe_axial_221_epsilon0_simple_root.py"
CERTIFICATE = ROOT / "artifacts/chronos/gfe_axial_221_epsilon0_simple_root_certificate.json"


def _receipt_value(output: str, key: str) -> str:
    prefix = key + " := "
    for line in output.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise AssertionError(f"missing receipt key: {key}")


def test_gfe_axial_221_epsilon0_simple_root_certificate() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    output = completed.stdout
    assert "RESULT := CERTIFIED_UNIQUE_SIMPLE_ROOT_DISK" in output

    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["scope"]["epsilon"] == 0.0
    assert record["scope"]["overtone"] == 1
    assert record["root_disk"]["unique_zero_counting_multiplicity"] == 1
    assert record["root_disk"]["simple_root"] is True
    assert record["gates"]["horizon_majorant_lt_one"] is True
    assert record["gates"]["infinity_damping_positive"] is True
    assert record["gates"]["rouche_margin_positive"] is True

    assert abs(
        float(_receipt_value(output, "HORIZON_MAJORANT_Q"))
        - record["gates"]["horizon_majorant_q_upper"]
    ) < 1e-15
    assert abs(
        float(_receipt_value(output, "INFINITY_DAMPING_LOWER"))
        - record["gates"]["infinity_damping_lower"]
    ) < 1e-15
    assert abs(
        float(_receipt_value(output, "ROUCHE_MARGIN"))
        - record["gates"]["rouche_margin_lower"]
    ) < 1e-15
