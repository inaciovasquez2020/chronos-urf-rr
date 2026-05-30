#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_baseline_residual_error_metrics_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONBaselineResidualErrorMetrics.lean")
DOC = Path("docs/status/MASCON_BASELINE_RESIDUAL_ERROR_METRICS_2026_05_29.md")

REQUIRED_METRICS = {
    "mean_absolute_error",
    "mean_squared_error",
    "root_mean_squared_error",
    "max_absolute_residual",
    "cosine_similarity",
    "pearson_correlation",
}

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "RESIDUAL_ERROR_METRICS_INTERFACE_ONLY_NO_NUMERIC_EXECUTION"
    assert artifact["vector_length"] == 66096000
    assert REQUIRED_METRICS <= set(artifact["metrics"])
    assert artifact["numeric_metrics_executed"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

    print("MASCON_BASELINE_RESIDUAL_ERROR_METRICS_OK")
    print(json.dumps({
        "status": artifact["status"],
        "metric_count": len(artifact["metrics"]),
        "numeric_metrics_executed": artifact["numeric_metrics_executed"],
        "model_comparison_executed": artifact["model_comparison_executed"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
