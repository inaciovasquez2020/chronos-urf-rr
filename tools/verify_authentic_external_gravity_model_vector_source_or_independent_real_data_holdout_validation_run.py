#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_independent_real_data_holdout_validation_run_2026_05_29.json")
DOC = Path("docs/status/AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorSourceOrIndependentRealDataHoldoutValidationRun.lean")
RUNNER = Path("tools/run_authentic_external_gravity_model_vector_source_or_independent_real_data_holdout_validation_run.py")

def finite_positive(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x)) and float(x) > 0.0

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert RUNNER.exists(), f"missing runner: {RUNNER}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_EXECUTED_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_NOT_SUPPLIED"
    assert artifact["branch_selected"] == "independent_real_data_holdout_validation_run"
    assert artifact["authentic_external_gravity_model_vector_source_supplied"] is False
    assert artifact["independent_real_data_holdout_validation_run_executed"] is True
    assert artifact["external_gravity_model_validation"] is False
    assert artifact["empirical_gravity_result"] is False

    assert artifact["authenticated_binding_artifact_count"] >= 1
    assert len(artifact["authenticated_binding_artifacts"]) == artifact["authenticated_binding_artifact_count"]

    holdout = artifact["holdout_validation"]
    assert holdout["rule"] == "time_index_mod_5_eq_0"
    assert holdout["holdout_vector_length"] == 13219200
    assert holdout["required_vector_length"] == 66096000
    assert holdout["required_shape"] == [255, 360, 720]
    assert holdout["positive_metric_check_passed"] is True
    assert finite_positive(holdout["mean_absolute_delta"])
    assert finite_positive(holdout["root_mean_square_delta"])

    assert artifact["bound_vectors"]["independent_baseline_file_exists"] is True
    assert artifact["bound_vectors"]["comparison_vector_file_exists"] is True
    assert artifact["bound_vectors"]["independent_baseline_path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["bound_vectors"]["comparison_vector_path"] == "data/mascon_vectors/deficit_vector.npy"

    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_EXTERNAL_MODEL_COMPARISON_REGISTRY"

    print("AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_OK")

if __name__ == "__main__":
    main()
