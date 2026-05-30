#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_execution_result_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonExecutionResult.lean")
DOC = Path("docs/status/MASCON_MODEL_COMPARISON_EXECUTION_RESULT_2026_05_29.md")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "MODEL_COMPARISON_EXECUTION_BLOCKED_NO_NUMERIC_VECTOR_PAYLOADS"
    assert artifact["comparison_executable"] is False
    assert artifact["numeric_metrics_executed"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["blocked_by_missing_numeric_payload"] is True
    assert artifact["empirical_gravity_result"] is False
    assert artifact["weakest_missing_object"] == "NUMERIC_MASCON_BASELINE_AND_DEFICIT_VECTOR_PAYLOADS"
    assert all(artifact["boundary"].values())

    print("MASCON_MODEL_COMPARISON_EXECUTION_RESULT_OK")
    print(json.dumps({
        "status": artifact["status"],
        "comparison_executable": artifact["comparison_executable"],
        "model_comparison_executed": artifact["model_comparison_executed"],
        "weakest_missing_object": artifact["weakest_missing_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
