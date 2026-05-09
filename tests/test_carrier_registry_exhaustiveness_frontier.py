import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_carrier_registry_exhaustiveness_frontier_artifact():
    data = json.loads((ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_frontier.json").read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["minimal_missing_lemma"] == "CarrierRegistryExhaustiveness"
    assert "zero-arity admissible predicate counterexample" in data["blocked_by"]
    assert "no theorem-level closure asserted" in data["boundary"]

def test_carrier_registry_exhaustiveness_frontier_doc_boundaries():
    text = (ROOT / "docs/status/CHRONOS_CARRIER_REGISTRY_EXHAUSTIVENESS_FRONTIER_2026_05_09.md").read_text()
    forbidden_promotions = [
        "proves CarrierRegistryExhaustiveness",
        "proves Reg-SNF",
        "proves UniversalFiberEntropyGap",
        "proves DepthBridge",
        "proves Chronos-RR",
        "proves H4.1/FGL",
        "proves P vs NP",
        "proves any Clay problem"
    ]
    for phrase in forbidden_promotions:
        assert phrase not in text
    assert "This file does not prove CarrierRegistryExhaustiveness." in text
