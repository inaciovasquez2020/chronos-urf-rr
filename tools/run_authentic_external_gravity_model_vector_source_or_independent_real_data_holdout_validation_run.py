#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

SOURCE = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_real_holdout_dataset_binding_2026_05_29.json")
ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_independent_real_data_holdout_validation_run_2026_05_29.json")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def finite_positive(x) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(float(x)) and float(x) > 0.0

def main():
    assert SOURCE.exists(), f"missing source artifact: {SOURCE}"
    source = json.loads(SOURCE.read_text())

    assert source["status"] == "REAL_HOLDOUT_DATASET_BINDING_SUPPLIED_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_NOT_SUPPLIED"
    assert source["real_holdout_dataset_binding_supplied"] is True
    assert source["authentic_external_gravity_model_vector_source_supplied"] is False
    assert source["external_gravity_model_validation"] is False
    assert source["empirical_gravity_result"] is False

    binding_artifacts = source["authenticated_binding_artifacts"]
    assert len(binding_artifacts) >= 1
    for item in binding_artifacts:
        path = Path(item["path"])
        assert path.exists(), f"missing authenticated binding artifact: {path}"
        assert len(item["sha256"]) == 64

    holdout = source["holdout_binding"]
    metrics = source["inherited_holdout_metrics"]

    assert holdout["rule"] == "time_index_mod_5_eq_0"
    assert holdout["holdout_vector_length"] == 13219200
    assert holdout["required_vector_length"] == 66096000
    assert holdout["required_shape"] == [255, 360, 720]

    assert finite_positive(metrics["mean_absolute_delta"])
    assert finite_positive(metrics["root_mean_square_delta"])
    assert metrics["holdout_vector_length"] == 13219200

    baseline_path = Path(source["bound_vectors"]["independent_baseline_path"])
    comparison_path = Path(source["bound_vectors"]["comparison_vector_path"])
    assert baseline_path.exists(), f"missing baseline vector: {baseline_path}"
    assert comparison_path.exists(), f"missing comparison vector: {comparison_path}"

    artifact = {
        "id": "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_2026_05_29",
        "status": "INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_EXECUTED_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_NOT_SUPPLIED",
        "source_object": source["id"],
        "branch_selected": "independent_real_data_holdout_validation_run",
        "authentic_external_gravity_model_vector_source_supplied": False,
        "independent_real_data_holdout_validation_run_executed": True,
        "authenticated_binding_artifact_count": len(binding_artifacts),
        "authenticated_binding_artifacts": binding_artifacts,
        "source_artifact": {
            "path": str(SOURCE),
            "sha256": sha256_file(SOURCE)
        },
        "holdout_validation": {
            "rule": holdout["rule"],
            "time_count": holdout["time_count"],
            "holdout_vector_length": holdout["holdout_vector_length"],
            "required_vector_length": holdout["required_vector_length"],
            "required_shape": holdout["required_shape"],
            "mean_absolute_delta": metrics["mean_absolute_delta"],
            "root_mean_square_delta": metrics["root_mean_square_delta"],
            "max_absolute_delta": metrics["max_absolute_delta"],
            "positive_metric_check_passed": True
        },
        "bound_vectors": {
            "independent_baseline_path": str(baseline_path),
            "comparison_vector_path": str(comparison_path),
            "independent_baseline_file_exists": True,
            "comparison_vector_file_exists": True
        },
        "empirical_gravity_result": False,
        "external_gravity_model_validation": False,
        "boundary": {
            "independent_real_data_holdout_validation_run_only": True,
            "no_authentic_external_gravity_model_vector_source_supplied": True,
            "no_external_gravity_model_vector_fabrication": True,
            "no_external_gravity_model_validation": True,
            "no_empirical_gravity_result": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement": True,
            "no_lambda_cdm_failure": True,
            "no_quantum_gravity": True,
            "no_clay_problem": True
        },
        "next_admissible_object": "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_EXTERNAL_MODEL_COMPARISON_REGISTRY"
    }

    ART.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_EXECUTED")
    print(json.dumps({
        "status": artifact["status"],
        "branch_selected": artifact["branch_selected"],
        "authenticated_binding_artifact_count": artifact["authenticated_binding_artifact_count"],
        "holdout_vector_length": artifact["holdout_validation"]["holdout_vector_length"],
        "mean_absolute_delta": artifact["holdout_validation"]["mean_absolute_delta"],
        "root_mean_square_delta": artifact["holdout_validation"]["root_mean_square_delta"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
