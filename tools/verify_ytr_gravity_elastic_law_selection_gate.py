#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/ytr_gravity_elastic_law_selection_gate_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/YtRGravityElasticLawSelectionGate.lean")
DOC = Path("docs/status/YTR_GRAVITY_ELASTIC_LAW_SELECTION_GATE_2026_05_29.md")
ROOT = Path("lean/Chronos.lean")

required_boundaries = [
    "observable prediction",
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

def main() -> None:
    artifact = json.loads(ART.read_text())
    lean = LEAN.read_text()
    doc = DOC.read_text()
    root = ROOT.read_text()

    assert artifact["id"] == "YTR_GRAVITY_ELASTIC_LAW_SELECTION_GATE_2026_05_29"
    assert artifact["status"] == "LAW_SELECTION_GATE_ONLY"
    assert artifact["next_admissible_object"] == "YtRGravityElasticObservablePrediction"

    assert "import Chronos.Frontier.YtRGravityElasticLawSelectionGate" in root
    assert "structure YtRGravityElasticLawSelectionGate" in lean
    assert "YtRMetricElasticLawSelectionGate" in lean
    assert "YtRTidalRestoringLawSelectionGate" in lean
    assert "selected_ytr_gravity_elastic_law_is_serious" in lean
    assert "selected_ytr_gravity_elastic_law_is_metric_or_tidal" in lean

    assert "LAW_SELECTION_GATE_ONLY" in doc
    assert "YtRGravityElasticObservablePrediction" in doc

    for boundary in required_boundaries:
        assert boundary in artifact["does_not_prove"]
        assert boundary in doc

    print("YTR_GRAVITY_ELASTIC_LAW_SELECTION_GATE_OK")

if __name__ == "__main__":
    main()
