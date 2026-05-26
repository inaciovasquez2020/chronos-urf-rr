import json
from pathlib import Path

ART = Path("artifacts/chronos/hybrid_hypersonic_propulsion_architecture_boundary_certificate_2026_05_26.json")
DOC = Path("docs/status/HYBRID_HYPERSONIC_PROPULSION_ARCHITECTURE_BOUNDARY_CERTIFICATE_2026_05_26.md")

def test_status_is_frontier_design_surface_only():
    data = json.loads(ART.read_text())
    assert data["status"] == "FRONTIER_DESIGN_SURFACE_ONLY"

def test_all_structural_actions_are_present():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    for token in [
        "REQUIREMENT_REGISTRY",
        "FAILURE_MODE_TAXONOMY",
        "THERMAL_BOUNDARY_CERTIFICATE",
        "CFD_VALIDATION_DEPENDENCY_SLOT",
        "WIND_TUNNEL_OR_FLIGHT_TEST_EVIDENCE_GATE",
        "LIGHT_CONE_RIGIDITY_DEPENDENCY_SLOT",
    ]:
        assert token in data["structural_actions"]
        assert token in doc

def test_no_propulsion_success_claim_is_promoted():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    for token in [
        "a better engine than a scramjet",
        "flight viability",
        "thrust advantage",
        "thermal survivability",
        "manufacturability",
        "aerospace validation",
        "military applicability",
        "hypersonic vehicle closure",
        "CFD validation",
        "wind-tunnel validation",
        "flight-test validation",
        "light-speed propulsion claim",
    ]:
        assert token in data["does_not_prove"]
        assert token in doc

def test_next_missing_object_is_light_cone_rigidity_dependency_slot():
    data = json.loads(ART.read_text())
    assert data["next_missing_object"] == "LIGHT_CONE_RIGIDITY_DEPENDENCY_SLOT"
