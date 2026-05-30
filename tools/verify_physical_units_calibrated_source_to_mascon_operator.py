#!/usr/bin/env python3
from pathlib import Path
import json
import math

ART = Path("artifacts/gravity/physical_units_calibrated_source_to_mascon_operator_2026_05_30.json")

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))

    assert artifact["object"] == "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_2026_05_30"
    assert artifact["status"] == "SOURCE_PHYSICAL_UNITS_OPERATOR_RECORDED_MASCON_UNIT_EQUIVALENCE_NOT_CLOSED"
    assert artifact["source_physical_units_operator_recorded"] is True
    assert artifact["finite_physical_vector_statistics_verified"] is True
    assert artifact["source_output_units"] == "mGal radial gravity disturbance proxy"
    assert artifact["source_to_grid_physical_units_calibrated"] is True
    assert artifact["source_to_mascon_shape_operator_recorded"] is True
    assert artifact["mascon_unit_equivalence_closed"] is False
    assert artifact["time_dependent_source_to_mascon_operator_closed"] is False
    assert artifact["comparison_metrics_recorded_on_normalized_alignment_vector"] is True
    assert artifact["source_name"] == "XGM2019e_2159"
    assert artifact["source_doi"] == "10.5880/ICGEM.2019.007"
    assert len(artifact["source_gfc_sha256"]) == 64
    assert len(artifact["physical_vector_sha256"]) == 64
    assert len(artifact["normalized_alignment_vector_sha256"]) == 64

    op = artifact["operator"]
    assert op["output_units"] == "mGal"
    assert op["numeric_rows_seen"] > 0
    assert op["synthesis_terms_used"] > 0
    assert op["raw_physical_grid_std_mgal"] > 0
    assert op["physical_vector_std_mgal_before_alignment_normalization"] > 0
    assert math.isfinite(op["raw_physical_grid_mean_mgal"])
    assert math.isfinite(op["raw_physical_grid_std_mgal"])
    assert math.isfinite(op["physical_vector_mean_mgal_before_alignment_normalization"])
    assert math.isfinite(op["physical_vector_std_mgal_before_alignment_normalization"])

    cmp = artifact["normalized_alignment_comparison"]
    assert cmp["lower_rmse_model"] in {"baseline", "deficit", "tie"}
    assert cmp["comparison_space"] == "dimensionless normalized alignment vector; not physical MASCON-unit equivalence"

    for group in ("baseline_metrics", "deficit_metrics"):
        assert cmp[group]["mean_absolute_delta"] >= 0
        assert cmp[group]["root_mean_square_delta"] >= 0
        assert math.isfinite(cmp[group]["mean_absolute_delta"])
        assert math.isfinite(cmp[group]["root_mean_square_delta"])

    boundary = artifact["boundary"]
    assert boundary["physical_source_units_operator_only"] is True
    assert boundary["mascon_unit_equivalence_not_closed"] is True
    assert boundary["time_dependent_operator_not_closed"] is True
    assert boundary["comparison_only"] is True
    assert boundary["no_empirical_gravity_result_claim"] is True
    assert boundary["no_gr_failure_claim"] is True
    assert boundary["no_new_gravity_claim"] is True
    assert boundary["no_dark_matter_replacement_claim"] is True
    assert boundary["no_lambda_cdm_failure_claim"] is True
    assert boundary["no_quantum_gravity_claim"] is True
    assert boundary["no_clay_claim"] is True
    assert boundary["independent_validation_required_before_physical_claim"] is True

    assert "MASCON vector physical units declaration" in artifact["missing_for_full_closure"]

    print("PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_OK")

if __name__ == "__main__":
    main()
