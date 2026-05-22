#!/usr/bin/env python3
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

REQUIRED_NONCLAIMS = [
    "unconditional stress-energy evolution identity",
    "WEC preservation under time evolution",
    "energy estimate dE/dt <= C E",
    "finite-time collapse theorem",
    "unrestricted gravity closure",
    "any Clay problem",
]

def main() -> None:
    for slug in SLUGS:
        path = ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json"
        assert path.exists(), path
        data = json.loads(path.read_text())

        assert data["repository"] == "chronos-urf-rr"
        assert data["route"] == "ROUTE_B_EXTERNAL_TENSOR_AUDIT"
        assert data["content"]
        assert data["remaining_blockers"]
        assert data["next_admissible_object"]

        nonclaims = "\n".join(data["does_not_prove"])
        for token in REQUIRED_NONCLAIMS:
            assert token in nonclaims

        boundary = "\n".join(data["boundary"])
        assert "no auditor contacted" in boundary
        assert "no audit response supplied" in boundary
        assert "no audit certificate supplied" in boundary
        assert "no theorem promotion" in boundary

    packet = json.loads((ROOT / "artifacts/chronos/clean_stress_energy_tensor_derivation_packet_content_2026_05_22.json").read_text())
    packet_content = packet["content"]
    assert "stress_energy_tensor" in packet_content
    assert "candidate_coordinate_identity" in packet_content
    assert "auditor_instruction" in packet_content

    request = json.loads((ROOT / "artifacts/chronos/external_tensor_audit_request_template_content_2026_05_22.json").read_text())
    assert "email_template" in request["content"]
    assert "not asking for endorsement of any collapse theorem" in request["content"]["email_template"]

    cert = json.loads((ROOT / "artifacts/chronos/external_tensor_audit_certificate_target_content_2026_05_22.json").read_text())
    assert "minimum_acceptance_rule" in cert["content"]
    assert "NO_CERTIFICATE_SUPPLIED" in cert["remaining_blockers"]

    lean = ROOT / "lean/Chronos/Frontier/RemainingRouteBAdmissibleObjects.lean"
    text = lean.read_text()
    assert "remaining_route_b_admissible_objects_recorded" in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()

    print("Remaining Route B admissible objects verification OK.")
    print("Status: PREPARATION_RECORDED_NO_CERTIFICATE")
    print("Next admissible object: EXTERNAL_AUDITOR_CONTACTS_SUPPLIED_OR_PACKET_SENT_RECORD")

if __name__ == "__main__":
    main()
