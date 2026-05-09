import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_zero_arity_carrier_obstruction_boundary_artifact():
    data = json.loads((ROOT / "artifacts/chronos/zero_arity_carrier_obstruction_boundary.json").read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["minimal_blocker"] == "ZeroArityCarrierObstruction"
    assert "represented by a registered carrier" in data["statement"]
    assert "formally excluded from RealChronosAdmissiblePredicate" in data["statement"]
    assert "no zero-arity resolution or theorem-level closure asserted" in data["boundary"]

def test_zero_arity_carrier_obstruction_boundary_doc_boundaries():
    text = (ROOT / "docs/status/CHRONOS_ZERO_ARITY_CARRIER_OBSTRUCTION_BOUNDARY_2026_05_09.md").read_text()
    required_negative_claims = [
        "This file does not resolve ZeroArityCarrierObstruction.",
        "This file does not prove ZeroArityRepresentation.",
        "This file does not prove ZeroArityExclusion.",
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

    forbidden_promotions = [
        "This file proves ZeroArityRepresentation",
        "This file proves ZeroArityExclusion",
        "This file proves CarrierRegistryExhaustiveness",
        "This file proves Reg-SNF",
        "This file proves UniversalFiberEntropyGap",
        "This file proves DepthBridge",
        "This file proves Chronos-RR",
        "This file proves H4.1/FGL",
        "This file proves P vs NP",
        "This file proves any Clay problem"
    ]
    for phrase in forbidden_promotions:
        assert phrase not in text
