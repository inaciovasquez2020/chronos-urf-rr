import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SLUGS = [
    "selected_external_tensor_audit_route",
    "clean_stress_energy_tensor_derivation_packet_content",
    "qualified_gr_auditor_contact_list_content_target",
    "external_tensor_audit_request_template_content",
    "external_tensor_audit_response_schema_content",
    "external_tensor_audit_certificate_target_content",
]

def artifact(slug):
    return json.loads((ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json").read_text())

def test_all_remaining_route_b_objects_exist():
    for slug in SLUGS:
        assert (ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json").exists()

def test_all_route_b_objects_have_content_and_no_certificate():
    for slug in SLUGS:
        data = artifact(slug)
        assert data["route"] == "ROUTE_B_EXTERNAL_TENSOR_AUDIT"
        assert data["content"]
        assert "no audit certificate supplied" in "\n".join(data["boundary"])

def test_clean_packet_contains_candidate_identity():
    data = artifact("clean_stress_energy_tensor_derivation_packet_content")
    content = data["content"]
    assert "stress_energy_tensor" in content
    assert "candidate_normal_identity" in content
    assert "candidate_coordinate_identity" in content
    assert "auditor_instruction" in content

def test_request_template_does_not_claim_theorem():
    data = artifact("external_tensor_audit_request_template_content")
    template = data["content"]["email_template"]
    assert "not asking for endorsement of any collapse theorem" in template
    assert "does not ask you to validate WEC preservation" in template

def test_certificate_target_requires_two_independent_positive_audits():
    data = artifact("external_tensor_audit_certificate_target_content")
    assert "At least two independent positive" in data["content"]["minimum_acceptance_rule"]
    assert "NO_POSITIVE_AUDIT_RESPONSES" in data["remaining_blockers"]
    assert "NO_CERTIFICATE_SUPPLIED" in data["remaining_blockers"]

def test_no_theorem_promotion_for_all_objects():
    for slug in SLUGS:
        data = artifact(slug)
        nonclaims = "\n".join(data["does_not_prove"])
        assert "unconditional stress-energy evolution identity" in nonclaims
        assert "WEC preservation under time evolution" in nonclaims
        assert "energy estimate dE/dt <= C E" in nonclaims
        assert "finite-time collapse theorem" in nonclaims
        assert "unrestricted gravity closure" in nonclaims
        assert "any Clay problem" in nonclaims

def test_lean_module_exists_without_admits():
    text = (ROOT / "lean/Chronos/Frontier/RemainingRouteBAdmissibleObjects.lean").read_text()
    assert "RemainingRouteBAdmissibleObject" in text
    assert "remaining_route_b_admissible_objects_recorded" in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()
