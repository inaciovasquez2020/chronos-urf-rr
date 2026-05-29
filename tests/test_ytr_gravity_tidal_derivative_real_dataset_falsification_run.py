from pathlib import Path
import json
import subprocess

ART = Path("artifacts/chronos/ytr_gravity_tidal_derivative_real_dataset_falsification_run_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/YtRGravityTidalDerivativeRealDatasetFalsificationRun.lean")

def test_artifact_status_and_dataset_binding():
    data = json.loads(ART.read_text())
    assert data["status"] == "REAL_DATA_FALSIFICATION_GATE_ONLY"
    assert data["changes"]["rename"]["to"] == "tidalDerivativeCoefficient"
    assert data["changes"]["public_dataset_payload_binding"]["dataset"] == "GRACEFO_L2_JPL_MONTHLY_0063"
    assert data["changes"]["falsification_certificate"]["disconfirmation_path_exists"] is True

def test_lean_surface_contains_required_objects():
    text = LEAN.read_text()
    assert "TidalDerivativeCoefficientRename" in text
    assert "EarthScaleTidalDerivativeConstants" in text
    assert "AuthenticPublicGravityDatasetPayloadBinding" in text
    assert "GRBaselineComparisonMetricWithTolerance" in text
    assert "ExplicitFalsificationCertificate" in text
    assert "YtRGravityTidalDerivativeRealDatasetFalsificationRun" in text

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_ytr_gravity_tidal_derivative_real_dataset_falsification_run.py"],
        check=True,
    )
