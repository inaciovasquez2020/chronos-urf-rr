import json
from pathlib import Path

ART = Path("artifacts/chronos/hypersonic_propulsion_validation_targets_2026_05_26.json")
DOC = Path("docs/status/HYPERSONIC_PROPULSION_VALIDATION_TARGETS_2026_05_26.md")

def test_status_is_targets_only_no_validation_supplied():
    data = json.loads(ART.read_text())
    assert data["status"] == "TARGETS_ONLY_NO_VALIDATION_SUPPLIED"
    assert "TARGETS_ONLY_NO_VALIDATION_SUPPLIED" in DOC.read_text()

def test_parent_boundary_certificate_is_linked():
    data = json.loads(ART.read_text())
    parent = "HYBRID_HYPERSONIC_PROPULSION_ARCHITECTURE_BOUNDARY_CERTIFICATE_2026_05_26"
    assert data["parent_boundary_certificate"] == parent
    assert parent in DOC.read_text()

def test_all_validation_targets_are_present_and_unsupplied():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    for target in [
        "CFD_VERIFICATION_VALIDATION_DOSSIER",
        "WIND_TUNNEL_TEST_REPORT",
        "FLIGHT_TEST_TELEMETRY_DOSSIER",
        "SCRAMJET_BASELINE_COMPARATIVE_BENCHMARK",
        "TRL_GATE_REGISTRY",
    ]:
        assert target in data["validation_targets"]
        assert data["missing_objects"][target] == "not supplied"
        assert target in doc

def test_no_propulsion_or_validation_claim_is_promoted():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    for claim in [
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
    ]:
        assert claim in data["does_not_prove"]
        assert claim in doc

def test_next_missing_object_is_cfd_dossier():
    data = json.loads(ART.read_text())
    assert data["next_missing_object"] == "CFD_VERIFICATION_VALIDATION_DOSSIER"
