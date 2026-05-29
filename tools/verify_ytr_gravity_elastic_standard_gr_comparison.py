#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/ytr_gravity_elastic_standard_gr_comparison_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/YtRGravityElasticStandardGRComparison.lean")
DOC = Path("docs/status/YTR_GRAVITY_ELASTIC_STANDARD_GR_COMPARISON_2026_05_29.md")
ROOT = Path("lean/Chronos.lean")

required_boundaries = [
    "empirical validation",
    "nontriviality certificate",
    "independent replication",
    "literal gravity elasticity",
    "standard GR failure",
    "new physics",
    "dark matter replacement",
    "Lambda-CDM failure",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

required_lean_tokens = [
    "YtRGravityElasticStandardGRBaselineKind",
    "YtRGravityElasticStandardGRComparisonMatches",
    "structure YtRGravityElasticStandardGRComparison",
    "YtRMetricElasticLensingStandardGRComparison",
    "YtRMetricElasticWavePhaseStandardGRComparison",
    "YtRTidalRestoringOrbitDriftStandardGRComparison",
    "YtRTidalRestoringRotationCurveStandardGRComparison",
    "YtRTidalRestoringWavePhaseStandardGRComparison",
    "ytr_gravity_elastic_standard_gr_comparison_has_observable_prediction",
    "ytr_gravity_elastic_standard_gr_comparison_has_serious_law",
    "ytr_gravity_elastic_standard_gr_comparison_matches_baseline",
]

def main() -> None:
    artifact = json.loads(ART.read_text())
    lean = LEAN.read_text()
    doc = DOC.read_text()
    root = ROOT.read_text()

    assert artifact["id"] == "YTR_GRAVITY_ELASTIC_STANDARD_GR_COMPARISON_2026_05_29"
    assert artifact["status"] == "STANDARD_GR_COMPARISON_GATE_ONLY"
    assert artifact["next_admissible_object"] == "YtRGravityElasticEmpiricalValidationRun"
    assert "YTR_GRAVITY_ELASTIC_OBSERVABLE_PREDICTION_2026_05_29" in artifact["depends_on"]
    assert "YTR_GRAVITY_ELASTIC_LAW_SELECTION_GATE_2026_05_29" in artifact["depends_on"]

    assert "import Chronos.Frontier.YtRGravityElasticStandardGRComparison" in root
    assert "import Chronos.Frontier.YtRGravityElasticObservablePrediction" in lean

    for token in required_lean_tokens:
        assert token in lean

    assert "STANDARD_GR_COMPARISON_GATE_ONLY" in doc
    assert "YtRGravityElasticEmpiricalValidationRun" in doc

    for boundary in required_boundaries:
        assert boundary in artifact["does_not_prove"]
        assert boundary in doc

    assert len(artifact["comparison_pairs"]) == 5

    print("YTR_GRAVITY_ELASTIC_STANDARD_GR_COMPARISON_OK")

if __name__ == "__main__":
    main()
