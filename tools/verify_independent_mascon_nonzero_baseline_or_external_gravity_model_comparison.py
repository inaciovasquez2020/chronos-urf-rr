#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/independent_mascon_nonzero_baseline_or_external_gravity_model_comparison_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/IndependentMASCONNonzeroBaselineOrExternalGravityModelComparison.lean")
DOC = Path("docs/status/INDEPENDENT_MASCON_NONZERO_BASELINE_OR_EXTERNAL_GRAVITY_MODEL_COMPARISON_2026_05_29.md")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "TARGET_ONLY_EXTERNAL_BASELINE_NOT_SUPPLIED"
    assert artifact["comparison_executable"] is False
    assert artifact["external_baseline_supplied"] is False
    assert artifact["empirical_gravity_result"] is False
    assert artifact["weakest_missing_object"] == "INDEPENDENT_NONZERO_MASCON_BASELINE_VECTOR_OR_EXTERNAL_GRAVITY_MODEL_VECTOR"
    assert all(artifact["boundary"].values())

    print("INDEPENDENT_MASCON_NONZERO_BASELINE_OR_EXTERNAL_GRAVITY_MODEL_COMPARISON_OK")
    print(json.dumps({
        "status": artifact["status"],
        "comparison_executable": artifact["comparison_executable"],
        "external_baseline_supplied": artifact["external_baseline_supplied"],
        "weakest_missing_object": artifact["weakest_missing_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
