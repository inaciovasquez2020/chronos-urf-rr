#!/usr/bin/env python3
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

REQUIRED_DEPENDENCIES = [
    "LEAN_FORMAL_STRESS_ENERGY_IDENTITY_OR_EXTERNAL_TENSOR_AUDIT",
    "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY",
    "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION",
    "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET",
    "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL",
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
        assert data["status"].endswith(("SUPPLIED", "RECORDED_NO_AUDIT_SUPPLIED", "RECORDED_NO_CONTACTS_SUPPLIED", "RECORDED_NO_REQUEST_SENT", "RECORDED_NO_RESPONSE_SUPPLIED", "RECORDED_NO_CERTIFICATE_SUPPLIED")) or "RECORDED" in data["status"]
        assert data["required_sections"]
        assert data["remaining_blockers"]

        for dep in REQUIRED_DEPENDENCIES:
            assert dep in data["depends_on"]

        nonclaims = "\n".join(data["does_not_prove"])
        for token in REQUIRED_NONCLAIMS:
            assert token in nonclaims

        boundary = "\n".join(data["boundary"])
        assert "no audit certificate supplied" in boundary
        assert "no theorem promotion" in boundary

    lean = ROOT / "lean/Chronos/Frontier/ExternalTensorAuditRouteObjects.lean"
    text = lean.read_text()
    assert "external_tensor_audit_route_objects_recorded" in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()

    print("External tensor audit route objects verification OK.")
    print("Status: ROUTE_B_INFRASTRUCTURE_RECORDED_NO_CERTIFICATE")
    print("Next admissible object: CLEAN_STRESS_ENERGY_TENSOR_DERIVATION_PACKET_CONTENT")

if __name__ == "__main__":
    main()
