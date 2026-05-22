import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SLUGS = [
    "clean_stress_energy_tensor_derivation_packet",
    "qualified_gr_auditor_contact_list",
    "external_tensor_audit_request_template",
    "external_tensor_audit_response_schema",
    "external_tensor_audit_certificate_target",
]

def artifact(slug):
    return json.loads((ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json").read_text())

def test_all_route_b_objects_exist():
    for slug in SLUGS:
        assert (ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json").exists()

def test_all_objects_are_route_b_infrastructure():
    for slug in SLUGS:
        data = artifact(slug)
        assert data["route"] == "ROUTE_B_EXTERNAL_TENSOR_AUDIT"
        assert "chronos-urf-rr" == data["repository"]

def test_derivation_packet_schema_has_required_sections():
    data = artifact("clean_stress_energy_tensor_derivation_packet")
    assert "fixed_sign_conventions" in data["required_sections"]
    assert "covariant_conservation_derivation" in data["required_sections"]
    assert "three_plus_one_decomposition" in data["required_sections"]
    assert "boundary_flux_terms" in data["required_sections"]

def test_auditor_contact_list_schema_has_required_sections():
    data = artifact("qualified_gr_auditor_contact_list")
    assert "auditor_name" in data["required_sections"]
    assert "institution" in data["required_sections"]
    assert "adm_or_3plus1_experience" in data["required_sections"]
    assert "conflict_of_interest_status" in data["required_sections"]

def test_request_response_and_certificate_targets_are_not_supplied():
    request = artifact("external_tensor_audit_request_template")
    response = artifact("external_tensor_audit_response_schema")
    cert = artifact("external_tensor_audit_certificate_target")
    assert "REQUEST_TEMPLATE_NOT_SENT" in request["remaining_blockers"]
    assert "NO_EXTERNAL_RESPONSE_SUPPLIED" in response["remaining_blockers"]
    assert "NO_POSITIVE_AUDIT_CERTIFICATES" in cert["remaining_blockers"]

def test_no_theorem_promotion_for_all_route_b_objects():
    for slug in SLUGS:
        data = artifact(slug)
        nonclaims = "\n".join(data["does_not_prove"])
        assert "unconditional stress-energy evolution identity" in nonclaims
        assert "WEC preservation under time evolution" in nonclaims
        assert "energy estimate dE/dt <= C E" in nonclaims
        assert "finite-time collapse theorem" in nonclaims
        assert "unrestricted gravity closure" in nonclaims
        assert "any Clay problem" in nonclaims

def test_lean_route_b_module_exists_without_admits():
    text = (ROOT / "lean/Chronos/Frontier/ExternalTensorAuditRouteObjects.lean").read_text()
    assert "ExternalTensorAuditObject" in text
    assert "external_tensor_audit_route_objects_recorded" in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()
