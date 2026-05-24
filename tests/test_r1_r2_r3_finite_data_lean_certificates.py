import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/r1_r2_r3_finite_data_lean_certificates_2026_05_24.json"

def test_finite_data_lean_certificates_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_r2_r3_finite_data_lean_certificates.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "R1_R2_R3_FINITE_DATA_LEAN_CERTIFICATES_OK" in result.stdout

def test_finite_data_lean_certificate_status_keeps_promotion_gap_open():
    data = json.loads(ART.read_text())
    assert data["status"] == "FINITE_DATA_LEAN_CERTIFIED_PROMOTION_GAP_OPEN"
    assert "R1R2R3FiniteDataToNativeProofPromotionGap" in data["open_promotion_gaps"]

def test_finite_data_lean_certificate_does_not_overclaim():
    data = json.loads(ART.read_text())
    blocked = set(data["does_not_prove"])
    assert "LongChordExclusion" in blocked
    assert "DiameterSeparationFillingObstruction" in blocked
    assert "UniformLocalTypeCapacity" in blocked
    assert "P vs NP" in blocked
    assert "any Clay problem" in blocked
