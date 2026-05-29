#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/ytr_gravity_elastic_observable_prediction_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/YtRGravityElasticObservablePrediction.lean")
DOC = Path("docs/status/YTR_GRAVITY_ELASTIC_OBSERVABLE_PREDICTION_2026_05_29.md")
ROOT = Path("lean/Chronos.lean")

required_boundaries = [
    "standard GR comparison",
    "empirical validation",
    "nontriviality certificate",
    "independent replication",
    "literal gravity elasticity",
    "new physics",
    "dark matter replacement",
    "Lambda-CDM failure",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

required_lean_tokens = [
    "YtRGravityElasticObservableKind",
    "YtRGravityElasticAllowedObservable",
    "structure YtRGravityElasticObservablePrediction",
    "YtRMetricElasticLensingObservablePrediction",
    "YtRMetricElasticWavePhaseObservablePrediction",
    "YtRTidalRestoringOrbitDriftObservablePrediction",
    "YtRTidalRestoringRotationCurveObservablePrediction",
    "YtRTidalRestoringWavePhaseObservablePrediction",
    "ytr_gravity_elastic_observable_prediction_has_serious_law",
    "ytr_gravity_elastic_observable_prediction_is_concrete",
    "ytr_gravity_elastic_observable_prediction_is_allowed",
]

def main() -> None:
    artifact = json.loads(ART.read_text())
    lean = LEAN.read_text()
    doc = DOC.read_text()
    root = ROOT.read_text()

    assert artifact["id"] == "YTR_GRAVITY_ELASTIC_OBSERVABLE_PREDICTION_2026_05_29"
    assert artifact["status"] == "OBSERVABLE_PREDICTION_GATE_ONLY"
    assert artifact["next_admissible_object"] == "YtRGravityElasticStandardGRComparison"
    assert "YTR_GRAVITY_ELASTIC_LAW_SELECTION_GATE_2026_05_29" in artifact["depends_on"]

    assert "import Chronos.Frontier.YtRGravityElasticObservablePrediction" in root
    assert "import Chronos.Frontier.YtRGravityElasticLawSelectionGate" in lean

    for token in required_lean_tokens:
        assert token in lean

    assert "OBSERVABLE_PREDICTION_GATE_ONLY" in doc
    assert "YtRGravityElasticStandardGRComparison" in doc

    for boundary in required_boundaries:
        assert boundary in artifact["does_not_prove"]
        assert boundary in doc

    assert len(artifact["candidate_observables"]) == 5

    print("YTR_GRAVITY_ELASTIC_OBSERVABLE_PREDICTION_OK")

if __name__ == "__main__":
    main()
