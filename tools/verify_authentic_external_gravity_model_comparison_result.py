from pathlib import Path
import json
import math

PROV = Path("artifacts/gravity/eigen6c4_external_gravity_vector_provenance_2026_05_30.json")
ART = Path("artifacts/gravity/authentic_external_gravity_model_comparison_result_2026_05_30.json")

def assert_boundary(boundary):
    for key in (
        "comparison_only",
        "no_external_gravity_model_fabrication",
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

    assert provenance["status"] == "SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_VECTOR_DERIVED_FROM_ICGEM_EIGEN6C4"
    assert provenance["source_name"] == "EIGEN-6C4"
    assert provenance["source_doi"] == "10.5880/icgem.2015.1"
    assert len(provenance["source_gfc_sha256"]) == 64
    assert len(provenance["external_vector_sha256"]) == 64
    assert provenance["shape"]["shape_compatible_with_baseline"] is True
    assert provenance["shape"]["shape_compatible_with_deficit"] is True
    assert_boundary(provenance["boundary"])

    assert artifact["object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_COMPARISON_RESULT_2026_05_30"
    assert artifact["status"] == "EXTERNAL_MODEL_COMPARISON_EXECUTED_BOUNDARY_LOCKED"
    assert artifact["comparison_executed"] is True
    assert artifact["external_source_name"] == "EIGEN-6C4"
    assert artifact["external_source_doi"] == "10.5880/icgem.2015.1"
    assert artifact["vector_length"] > 0
    assert artifact["lower_rmse_model"] in {"baseline", "deficit", "tie"}

    for group in ("baseline_metrics", "deficit_metrics"):
        assert artifact[group]["mean_absolute_delta"] >= 0
        assert artifact[group]["root_mean_square_delta"] >= 0
        assert math.isfinite(artifact[group]["mean_absolute_delta"])
        assert math.isfinite(artifact[group]["root_mean_square_delta"])

    assert_boundary(artifact["boundary"])

    print("AUTHENTIC_EXTERNAL_GRAVITY_MODEL_COMPARISON_RESULT_OK")

if __name__ == "__main__":
    main()
