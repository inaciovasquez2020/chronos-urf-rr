#!/usr/bin/env python3
from pathlib import Path
import json
import math

ART = Path("artifacts/gravity/physical_units_calibrated_source_to_mascon_operator_or_third_public_holdout_2026_05_30.json")
MANIFEST = Path("artifacts/gravity/third_public_holdout_reproducibility_manifest_2026_05_30.json")

def assert_boundary(boundary):
    for key in (
        "third_public_holdout_only",
        "comparison_only",
        "physical_units_calibrated_operator_not_closed",
        "no_empirical_gravity_result_claim",
        "no_gr_failure_claim",
        "no_new_gravity_claim",
        "no_dark_matter_replacement_claim",
        "no_lambda_cdm_failure_claim",
        "no_quantum_gravity_claim",
        "no_clay_claim",
    ):
        assert boundary[key] is True

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert artifact["object"] == "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OR_THIRD_PUBLIC_HOLDOUT_2026_05_30"
    assert artifact["status"] == "THIRD_PUBLIC_HOLDOUT_EXECUTED_PHYSICAL_UNITS_CALIBRATED_OPERATOR_NOT_CLOSED"
    assert artifact["third_public_holdout_executed"] is True
    assert artifact["physical_units_calibrated_source_to_mascon_operator_closed"] is False
    assert artifact["source_to_mascon_operator_audit_recorded"] is True
    assert artifact["third_public_holdout_reproducibility_manifest_recorded"] is True
    assert artifact["comparison_result_interpretation_boundary_locked"] is True
    assert artifact["source_name"] == "XGM2019e_2159"
    assert artifact["source_doi"] == "10.5880/ICGEM.2019.007"
    assert len(artifact["source_gfc_sha256"]) == 64
    assert len(artifact["external_vector_sha256"]) == 64
    assert artifact["vector_length"] > 0
    assert artifact["current_lower_rmse_model"] in {"baseline", "deficit", "tie"}
    assert isinstance(artifact["agrees_with_prior_lower_rmse_models"], bool)

    audit = artifact["source_to_mascon_operator_audit"]
    assert audit["numeric_rows_seen"] > 0
    assert audit["synthesis_terms_used"] > 0
    assert audit["raw_grid_std_before_normalization"] > 0

    gate = artifact["physical_units_calibration_gate"]
    assert gate["calibration_status"] == "NOT_CLOSED"
    assert gate["missing_for_closure"]

    for group in ("baseline_metrics", "deficit_metrics"):
        assert artifact[group]["mean_absolute_delta"] >= 0
        assert artifact[group]["root_mean_square_delta"] >= 0
        assert math.isfinite(artifact[group]["mean_absolute_delta"])
        assert math.isfinite(artifact[group]["root_mean_square_delta"])

    assert_boundary(artifact["boundary"])
    assert artifact["boundary"]["independent_validation_required_before_physical_claim"] is True

    assert manifest["object"] == "THIRD_PUBLIC_HOLDOUT_REPRODUCIBILITY_MANIFEST_2026_05_30"
    assert manifest["status"] == "THIRD_PUBLIC_HOLDOUT_REPRODUCIBILITY_MANIFEST_RECORDED"
    assert manifest["downloads"][0]["source_name"] == "XGM2019e_2159"
    assert len(manifest["downloads"][0]["sha256"]) == 64
    assert len(manifest["generated_vectors"][0]["sha256"]) == 64
    assert manifest["operator"]["physical_units_calibration_status"] == "NOT_CLOSED"
    assert_boundary(manifest["boundary"])

    print("PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OR_THIRD_PUBLIC_HOLDOUT_OK")

if __name__ == "__main__":
    main()
