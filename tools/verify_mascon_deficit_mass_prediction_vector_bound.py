#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/mascon_deficit_mass_prediction_vector_bound_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONDeficitMassPredictionVectorBound.lean")
DOC = Path("docs/status/MASCON_DEFICIT_MASS_PREDICTION_VECTOR_BOUND_2026_05_29.md")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "VECTOR_BOUND_FROM_CONCRETE_LAW_INTERFACE_NO_MODEL_COMPARISON"
    assert artifact["source_law"] == "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW_2026_05_29"
    assert artifact["shape"] == {"time": 255, "lat": 360, "lon": 720}
    assert artifact["vector_length"] == 255 * 360 * 720
    assert artifact["numeric_payload_in_git"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

    print("MASCON_DEFICIT_MASS_PREDICTION_VECTOR_BOUND_OK")
    print(json.dumps({
        "status": artifact["status"],
        "vector_length": artifact["vector_length"],
        "model_comparison_executed": artifact["model_comparison_executed"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2))

if __name__ == "__main__":
    main()
