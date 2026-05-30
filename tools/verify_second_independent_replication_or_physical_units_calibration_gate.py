#!/usr/bin/env python3
from pathlib import Path
import json
import math

ART = Path("artifacts/gravity/second_independent_replication_or_physical_units_calibration_gate_2026_05_30.json")
MANIFEST = Path("artifacts/gravity/public_gravity_external_download_reproducibility_manifest_2026_05_30.json")

def assert_boundary(boundary):
    for key in (
        "comparison_only",
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

    assert artifact["object"] == "SECOND_INDEPENDENT_REPLICATION_OR_PHYSICAL_UNITS_CALIBRATION_GATE_2026_05_30"
    assert artifact["status"] == "SECOND_INDEPENDENT_REPLICATION_EXECUTED_PHYSICAL_UNITS_CALIBRATION_GATE_RECORDED_NOT_CLOSED"
    assert artifact["second_independent_replication_executed"] is True
    assert artifact["physical_units_calibration_gate_recorded"] is True
    assert artifact["physical_units_calibration_closed"] is False
    assert artifact["source_to_mascon_operator_audit_recorded"] is True
    assert artifact["public_reproducibility_manifest_recorded"] is True
    assert artifact["comparison_result_interpretation_boundary_locked"] is True
    assert artifact["source_name"] == "ITSG-Grace2018s"
    assert artifact["source_doi"] == "10.5880/ICGEM.2018.003"
    assert len(artifact["source_gfc_sha256"]) == 64
    assert len(artifact["external_vector_sha256"]) == 64
    assert artifact["vector_length"] > 0
    assert artifact["current_lower_rmse_model"] in {"baseline", "deficit", "tie"}
    assert isinstance(artifact["agrees_with_prior_lower_rmse_models"], bool)
    assert artifact["source_to_mascon_operator_audit"]["numeric_rows_seen"] > 0
    assert artifact["source_to_mascon_operator_audit"]["synthesis_terms_used"] > 0
    assert artifact["source_to_mascon_operator_audit"]["raw_grid_std_before_normalization"] > 0
    assert artifact["physical_units_calibration_gate"]["calibration_status"] == "RECORDED_NOT_CLOSED"

    for group in ("baseline_metrics", "deficit_metrics"):
        assert artifact[group]["mean_absolute_delta"] >= 0
        assert artifact[group]["root_mean_square_delta"] >= 0
        assert math.isfinite(artifact[group]["mean_absolute_delta"])
        assert math.isfinite(artifact[group]["root_mean_square_delta"])

    assert_boundary(artifact["boundary"])
    assert artifact["boundary"]["physical_units_calibration_not_closed"] is True
    assert artifact["boundary"]["independent_validation_required_before_physical_claim"] is True

    assert manifest["object"] == "PUBLIC_GRAVITY_EXTERNAL_DOWNLOAD_REPRODUCIBILITY_MANIFEST_2026_05_30"
    assert manifest["status"] == "PUBLIC_REPRODUCIBILITY_MANIFEST_RECORDED"
    assert manifest["downloads"]
    assert manifest["generated_vectors"]
    assert manifest["operator"]["physical_units_calibration_status"] == "RECORDED_NOT_CLOSED"
    assert_boundary(manifest["boundary"])
    assert manifest["boundary"]["physical_units_calibration_not_closed"] is True

    print("SECOND_INDEPENDENT_REPLICATION_OR_PHYSICAL_UNITS_CALIBRATION_GATE_OK")

if __name__ == "__main__":
    main()
