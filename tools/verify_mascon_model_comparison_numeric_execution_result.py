#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_numeric_execution_result_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonNumericExecutionResult.lean")
DOC = Path("docs/status/MASCON_MODEL_COMPARISON_NUMERIC_EXECUTION_RESULT_2026_05_29.md")

def finite_or_none(x):
    return x is None or (isinstance(x, (int, float)) and math.isfinite(float(x)))

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "NUMERIC_MODEL_COMPARISON_EXECUTED_NO_EMPIRICAL_CLAIM"
    assert artifact["vector_length"] == 66096000
    assert artifact["numeric_metrics_executed"] is True
    assert artifact["model_comparison_executed"] is True
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

    metrics = artifact["metrics"]
    for key in [
        "mean_absolute_error",
        "mean_squared_error",
        "root_mean_squared_error",
        "max_absolute_residual",
        "baseline_l2_norm",
        "deficit_l2_norm",
        "residual_l2_norm",
    ]:
        assert math.isfinite(float(metrics[key])), key

    assert finite_or_none(metrics["cosine_similarity"])
    assert finite_or_none(metrics["pearson_correlation"])

    print("MASCON_MODEL_COMPARISON_NUMERIC_EXECUTION_RESULT_OK")
    print(json.dumps({
        "status": artifact["status"],
        "vector_length": artifact["vector_length"],
        "numeric_metrics_executed": artifact["numeric_metrics_executed"],
        "model_comparison_executed": artifact["model_comparison_executed"],
        "empirical_gravity_result": artifact["empirical_gravity_result"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
