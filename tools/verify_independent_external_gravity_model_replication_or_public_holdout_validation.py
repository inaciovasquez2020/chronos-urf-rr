from pathlib import Path
import json
import math

PROV = Path("artifacts/gravity/goco06s_independent_external_gravity_vector_provenance_2026_05_30.json")
ART = Path("artifacts/gravity/independent_external_gravity_model_replication_or_public_holdout_validation_2026_05_30.json")

def assert_boundary(boundary):
    for key in (
        "replication_or_public_holdout_only",
        "comparison_only",
        "no_empirical_gravity_result_claim",
        "no_gr_failure_claim",
        "no_new_gravity_claim",
        "no_dark_matter_replacement_claim",
        "no_lambda_cdm_failure_claim",
        "no_quantum_gravity_claim",
        "no_clay_claim",
        "independent_validation_required_before_physical_claim",
    ):
        assert boundary[key] is True

def main() -> None:
    provenance = json.loads(PROV.read_text(encoding="utf-8"))
    artifact = json.loads(ART.read_text(encoding="utf-8"))

    assert provenance["status"] == "SHAPE_COMPATIBLE_PUBLIC_HOLDOUT_GRAVITY_VECTOR_DERIVED_FROM_ICGEM_GOCO06S"
    assert provenance["source_name"] == "GOCO06s"
    assert provenance["source_doi"] == "10.5880/ICGEM.2019.002"
    assert len(provenance["source_gfc_sha256"]) == 64
    assert len(provenance["external_vector_sha256"]) == 64
    assert provenance["synthesis"]["numeric_rows_seen"] > 0
    assert provenance["synthesis"]["synthesis_terms_used"] > 0
    assert provenance["synthesis"]["raw_grid_std_before_normalization"] > 0
    assert provenance["shape"]["shape_compatible_with_baseline"] is True
    assert provenance["shape"]["shape_compatible_with_deficit"] is True
    assert_boundary(provenance["boundary"])

    assert artifact["object"] == "INDEPENDENT_EXTERNAL_GRAVITY_MODEL_REPLICATION_OR_PUBLIC_HOLDOUT_VALIDATION_2026_05_30"
    assert artifact["status"] == "INDEPENDENT_PUBLIC_HOLDOUT_VALIDATION_EXECUTED_BOUNDARY_LOCKED"
    assert artifact["replication_or_public_holdout_validation_executed"] is True
    assert artifact["replication_source_name"] == "GOCO06s"
    assert artifact["replication_source_doi"] == "10.5880/ICGEM.2019.002"
    assert artifact["vector_length"] > 0
    assert artifact["lower_rmse_model"] in {"baseline", "deficit", "tie"}
    assert artifact["prior_lower_rmse_model"] in {"baseline", "deficit", "tie", "unknown"}
    assert isinstance(artifact["replicates_prior_lower_rmse_model"], bool)

    for group in ("baseline_metrics", "deficit_metrics"):
        assert artifact[group]["mean_absolute_delta"] >= 0
        assert artifact[group]["root_mean_square_delta"] >= 0
        assert math.isfinite(artifact[group]["mean_absolute_delta"])
        assert math.isfinite(artifact[group]["root_mean_square_delta"])

    assert_boundary(artifact["boundary"])

    print("INDEPENDENT_EXTERNAL_GRAVITY_MODEL_REPLICATION_OR_PUBLIC_HOLDOUT_VALIDATION_OK")

if __name__ == "__main__":
    main()
