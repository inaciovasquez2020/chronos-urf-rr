#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_repair_field_package_bridge_2026_06_25.json")
SOURCE = Path("lean/Chronos/Frontier/H4_1_FGL_SelectedDomainRestriction.lean")

EXPECTED = {
    "artifact": "SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_2026_06_25",
    "repository": "chronos-urf-rr",
    "lean_target": "Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction",
    "source_file": str(SOURCE),
    "bridge_theorem": "selected_domain_defect_repair_target_from_field_package",
    "target_boundary": "SELECTED_DOMAIN_DEFECT_REPAIR_TO_REALIZABLE_NORMALIZATION_BOUNDARY",
    "field_package": "SelectedDomainDefectRepairTargetField",
    "provider_assumption": "∀ w : W_unrestricted, terminal_unrestricted w → selected_domain_representable w → SelectedDomainDefectRepairTargetField w",
}

EXPECTED_FIELDS = [
    "repaired : W_unrestricted",
    "repaired_realizable : selected_domain_realizable repaired",
    "repaired_terminal : terminal_unrestricted repaired",
    "nf : W_T",
    "nf_represents_original : represents_terminal nf w",
    "original_normalizes_to_nf : normalization_relation w nf",
]

EXPECTED_NON_CLAIMS = [
    "does not construct a field-package provider",
    "does not prove unrestricted repair existence",
    "does not prove selected-domain representability",
    "does not prove terminal closure from arbitrary input",
    "does not prove normalization independently of the package",
    "does not attempt SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM",
]

EXPECTED_SOURCE_TOKENS = [
    "structure SelectedDomainDefectRepairTargetField",
    "theorem selected_domain_defect_repair_target_from_field_package",
    "SELECTED_DOMAIN_DEFECT_REPAIR_TO_REALIZABLE_NORMALIZATION_BOUNDARY",
    *EXPECTED_FIELDS,
]

def fail(message: str) -> None:
    raise SystemExit(f"SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_2026_06_25_FAIL: {message}")

def main() -> None:
    if not ARTIFACT.is_file():
        fail(f"missing artifact {ARTIFACT}")
    if not SOURCE.is_file():
        fail(f"missing source {SOURCE}")

    data = json.loads(ARTIFACT.read_text())
    source_text = SOURCE.read_text()

    for key, value in EXPECTED.items():
        if data.get(key) != value:
            fail(f"{key} mismatch")

    source_sha256 = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if data.get("source_sha256") != source_sha256:
        fail("source_sha256 mismatch")

    if data.get("field_package_fields") != EXPECTED_FIELDS:
        fail("field_package_fields mismatch")

    if data.get("non_claims") != EXPECTED_NON_CLAIMS:
        fail("non_claims mismatch")

    validation = data.get("validation")
    if validation != ["lake build Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction"]:
        fail("validation command mismatch")

    missing_tokens = [token for token in EXPECTED_SOURCE_TOKENS if token not in source_text]
    if missing_tokens:
        fail("missing source token(s): " + ", ".join(missing_tokens))

    print("SELECTED_DOMAIN_REPAIR_FIELD_PACKAGE_BRIDGE_2026_06_25_OK")

if __name__ == "__main__":
    main()
