import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools/gfe/verify_gfe_axial_221_epsilon0_root_refinement.py"
CERTIFICATE = ROOT / "artifacts/chronos/gfe_axial_221_epsilon0_root_refinement_certificate.json"

def value(output: str, key: str) -> float:
    prefix = key + " := "
    for line in output.splitlines():
        if line.startswith(prefix):
            return float(line[len(prefix):])
    raise AssertionError(f"missing receipt key: {key}")

def test_axial_221_epsilon0_root_refinement() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT, check=True, capture_output=True, text=True, timeout=120,
    )
    out = completed.stdout
    assert "RESULT := CERTIFIED_UNIQUE_SIMPLE_ROOT_REFINEMENT" in out
    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert record["root_disk"]["radius"] == 1.1e-6
    assert record["root_disk"]["simple_root"] is True
    assert value(out, "HORIZON_MAJORANT_Q") < record["conservative_gates"]["horizon_majorant_q_upper_bound"]
    assert value(out, "INFINITY_DAMPING_LOWER") > record["conservative_gates"]["infinity_damping_lower_bound"]
    assert value(out, "ROUCHE_MARGIN") > record["conservative_gates"]["rouche_margin_lower_bound"]
