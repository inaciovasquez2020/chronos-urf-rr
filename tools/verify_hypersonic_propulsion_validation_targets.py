#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/hypersonic_propulsion_validation_targets_2026_05_26.json")
DOC = Path("docs/status/HYPERSONIC_PROPULSION_VALIDATION_TARGETS_2026_05_26.md")

data = json.loads(ART.read_text())
doc = DOC.read_text()

assert data["status"] == "TARGETS_ONLY_NO_VALIDATION_SUPPLIED"
assert data["parent_boundary_certificate"] == "HYBRID_HYPERSONIC_PROPULSION_ARCHITECTURE_BOUNDARY_CERTIFICATE_2026_05_26"
assert "TARGETS_ONLY_NO_VALIDATION_SUPPLIED" in doc
assert "HYBRID_HYPERSONIC_PROPULSION_ARCHITECTURE_BOUNDARY_CERTIFICATE_2026_05_26" in doc

required_targets = [
    "CFD_VERIFICATION_VALIDATION_DOSSIER",
    "WIND_TUNNEL_TEST_REPORT",
    "FLIGHT_TEST_TELEMETRY_DOSSIER",
    "SCRAMJET_BASELINE_COMPARATIVE_BENCHMARK",
    "TRL_GATE_REGISTRY",
]

for target in required_targets:
    assert target in data["validation_targets"], target
    assert target in data["missing_objects"], target
    assert data["missing_objects"][target] == "not supplied", target
    assert target in doc, target

required_nonclaims = [
    "CFD validation",
    "wind-tunnel validation",
    "flight-test validation",
    "scramjet superiority",
    "flight viability",
    "propulsion breakthrough",
    "thrust advantage",
    "thermal survivability",
    "manufacturability",
    "aerospace validation",
    "military applicability",
    "hypersonic vehicle closure",
    "light-speed propulsion claim",
]

for claim in required_nonclaims:
    assert claim in data["does_not_prove"], claim
    assert claim in doc, claim

assert data["next_missing_object"] == "CFD_VERIFICATION_VALIDATION_DOSSIER"
assert "This registry identifies external validation targets only." in doc

print("HYPERSONIC_PROPULSION_VALIDATION_TARGETS_OK")
