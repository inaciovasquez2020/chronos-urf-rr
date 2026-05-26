#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/hybrid_hypersonic_propulsion_architecture_boundary_certificate_2026_05_26.json")
DOC = Path("docs/status/HYBRID_HYPERSONIC_PROPULSION_ARCHITECTURE_BOUNDARY_CERTIFICATE_2026_05_26.md")

data = json.loads(ART.read_text())
doc = DOC.read_text()

assert data["status"] == "FRONTIER_DESIGN_SURFACE_ONLY"

required_actions = [
    "REQUIREMENT_REGISTRY",
    "FAILURE_MODE_TAXONOMY",
    "THERMAL_BOUNDARY_CERTIFICATE",
    "CFD_VALIDATION_DEPENDENCY_SLOT",
    "WIND_TUNNEL_OR_FLIGHT_TEST_EVIDENCE_GATE",
    "LIGHT_CONE_RIGIDITY_DEPENDENCY_SLOT",
]

for token in required_actions:
    assert token in data["structural_actions"], token
    assert token in doc, token

for forbidden_claim in [
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
    assert forbidden_claim in data["does_not_prove"], forbidden_claim
    assert forbidden_claim in doc, forbidden_claim

assert data["next_missing_object"] == "LIGHT_CONE_RIGIDITY_DEPENDENCY_SLOT"
assert "FRONTIER_DESIGN_SURFACE_ONLY" in doc

print("HYBRID_HYPERSONIC_PROPULSION_ARCHITECTURE_BOUNDARY_CERTIFICATE_OK")
