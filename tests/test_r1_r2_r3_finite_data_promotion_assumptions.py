import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/r1_r2_r3_finite_data_promotion_assumptions_2026_05_24.json"

def test_finite_data_promotion_assumptions_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_r2_r3_finite_data_promotion_assumptions.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_R2_R3_FINITE_DATA_PROMOTION_ASSUMPTIONS_OK" in result.stdout

def test_promotion_assumption_layer_keeps_non_factorisation_conditional():
    data = json.loads(ART.read_text())
    assert data["status"] == "PROMOTION_ASSUMPTION_LAYER_ONLY_NON_FACTORISATION_CONDITIONAL"
    assert "proof of NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance" in data["remaining_open_objects"]

def test_promotion_assumption_layer_does_not_overclaim():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "LongChordExclusion" in blocked
    assert "DiameterSeparationFillingObstruction" in blocked
    assert "UniformLocalTypeCapacity" in blocked
    assert "NON_FACTORISATION unconditionally" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
