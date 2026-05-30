#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_interpretation_boundary_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonInterpretationBoundary.lean")
DOC = Path("docs/status/MASCON_MODEL_COMPARISON_INTERPRETATION_BOUNDARY_2026_05_29.md")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "INTERPRETATION_BOUNDARY_CLOSED_NO_EMPIRICAL_GRAVITY_CLAIM"
    assert artifact["external_baseline_comparison"] is False
    assert artifact["empirical_gravity_result"] is False
    assert "does not compare against GR" in artifact["forbidden_interpretation"]
    assert all(artifact["boundary"].values())

    metrics = artifact["metrics_recorded"]
    assert math.isfinite(metrics["mean_absolute_error"])
    assert math.isfinite(metrics["root_mean_squared_error"])
    assert math.isfinite(metrics["max_absolute_residual"])

    print("MASCON_MODEL_COMPARISON_INTERPRETATION_BOUNDARY_OK")
    print(json.dumps({
        "status": artifact["status"],
        "external_baseline_comparison": artifact["external_baseline_comparison"],
        "empirical_gravity_result": artifact["empirical_gravity_result"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
