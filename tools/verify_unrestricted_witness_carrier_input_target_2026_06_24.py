#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "unrestricted_witness_carrier_input_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "UNRESTRICTED_WITNESS_CARRIER_INPUT_TARGET_2026_06_24.md"

REQUIRED_SURFACE = {
    "carrier": "W_unrestricted",
    "terminal_predicate": "terminal_unrestricted",
    "selected_domain_representability_predicate": "selected_domain_representable",
    "normalization_relation": "normalization_relation",
    "discharge_equivalence": "discharge_equivalent",
    "discharge_predicate": "discharged_unrestricted",
}

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "UNRESTRICTED_WITNESS_CARRIER_INPUT_TARGET_2026_06_24"
    assert data["parent_status"] == "SELECTED_DOMAIN_DEFECT_BASIS_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["carrier_surface"] == REQUIRED_SURFACE
    assert data["required_next_object"]["name"] == "SelectedDomainDefect"
    assert data["weakest_missing_object"]["name"] == "SELECTED_DOMAIN_DEFECT_BASIS"

    for token in [
        "BOUNDARY := not SelectedDomainDefect_defined",
        "BOUNDARY := not defect_atoms_defined",
        "BOUNDARY := not selected_domain_defect_defined",
        "BOUNDARY := not SELECTED_DOMAIN_DEFECT_BASIS_proved",
        "BOUNDARY := not unrestricted_terminal_closure_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "W_unrestricted",
        "terminal_unrestricted",
        "selected_domain_representable",
        "normalization_relation",
        "discharge_equivalent",
        "discharged_unrestricted",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved",
    ]:
        assert token in doc

    print("UNRESTRICTED_WITNESS_CARRIER_INPUT_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
