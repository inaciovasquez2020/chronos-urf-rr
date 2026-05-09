import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_admissibility_positivity_decision_lock_artifact():
    data = json.loads((ROOT / "artifacts/chronos/admissibility_positivity_decision_lock.json").read_text())
    assert data["status"] == "DECISION_LOCKED"
    assert data["blocked_theorem"] == "ZeroArityExclusion"
    assert data["viable_route_without_semantic_change"] == "ZeroArityRepresentation"
    assert "PositiveArityAdmissibility" in data["minimal_missing_assumption_for_exclusion"]
    assert "Decision lock only" in data["boundary"]
def test_admissibility_positivity_decision_lock_doc_boundaries():
    text = (ROOT / "docs/status/CHRONOS_ADMISSIBILITY_POSITIVITY_DECISION_LOCK_2026_05_09.md").read_text()
    required_negative_claims = [
    "This file does not prove ZeroArityExclusion.",
    "This file does not prove ZeroArityRepresentation.",
    "This file does not resolve ZeroArityCarrierObstruction.",
    "This file does not prove CarrierRegistryExhaustiveness.",
    "This file does not prove Reg-SNF.",
    "This file does not prove UniversalFiberEntropyGap.",
    "This file does not prove DepthBridge.",
    "This file does not prove Chronos-RR.",
    "This file does not prove H4.1/FGL.",
    "This file does not prove P vs NP.",
    "This file does not prove any Clay problem."
    ]
    for claim in required_negative_claims:
        assert claim in text
    assert "Current RealChronosAdmissiblePredicate semantics permit zero-arity." in text
    assert "PositiveArityAdmissibility:" in text
    assert "ZeroArityRepresentation:" in text
