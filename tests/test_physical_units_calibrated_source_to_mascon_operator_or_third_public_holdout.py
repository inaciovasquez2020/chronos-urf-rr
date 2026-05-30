import json
from pathlib import Path

ART = Path("artifacts/gravity/physical_units_calibrated_source_to_mascon_operator_or_third_public_holdout_2026_05_30.json")
MANIFEST = Path("artifacts/gravity/third_public_holdout_reproducibility_manifest_2026_05_30.json")

def test_third_public_holdout_artifact():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    assert artifact["status"] == "THIRD_PUBLIC_HOLDOUT_EXECUTED_PHYSICAL_UNITS_CALIBRATED_OPERATOR_NOT_CLOSED"
    assert artifact["third_public_holdout_executed"] is True
    assert artifact["physical_units_calibrated_source_to_mascon_operator_closed"] is False
    assert artifact["source_name"] == "XGM2019e_2159"
    assert artifact["source_doi"] == "10.5880/ICGEM.2019.007"
    assert artifact["vector_length"] > 0
    assert artifact["current_lower_rmse_model"] in {"baseline", "deficit", "tie"}

def test_operator_audit_and_calibration_gate():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    audit = artifact["source_to_mascon_operator_audit"]
    gate = artifact["physical_units_calibration_gate"]
    assert audit["numeric_rows_seen"] > 0
    assert audit["synthesis_terms_used"] > 0
    assert audit["raw_grid_std_before_normalization"] > 0
    assert gate["calibration_status"] == "NOT_CLOSED"
    assert gate["missing_for_closure"]

def test_third_public_holdout_manifest():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "THIRD_PUBLIC_HOLDOUT_REPRODUCIBILITY_MANIFEST_RECORDED"
    assert manifest["downloads"][0]["source_name"] == "XGM2019e_2159"
    assert len(manifest["downloads"][0]["sha256"]) == 64
    assert len(manifest["generated_vectors"][0]["sha256"]) == 64
    assert manifest["operator"]["physical_units_calibration_status"] == "NOT_CLOSED"

def test_boundaries():
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    boundary = artifact["boundary"]
    assert boundary["third_public_holdout_only"] is True
    assert boundary["comparison_only"] is True
    assert boundary["physical_units_calibrated_operator_not_closed"] is True
    assert boundary["no_empirical_gravity_result_claim"] is True
    assert boundary["no_gr_failure_claim"] is True
    assert boundary["no_new_gravity_claim"] is True
    assert boundary["no_dark_matter_replacement_claim"] is True
    assert boundary["no_lambda_cdm_failure_claim"] is True
    assert boundary["no_quantum_gravity_claim"] is True
    assert boundary["no_clay_claim"] is True
    assert boundary["independent_validation_required_before_physical_claim"] is True
