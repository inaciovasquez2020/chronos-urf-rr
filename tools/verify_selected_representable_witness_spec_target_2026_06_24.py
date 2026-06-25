#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "selected_representable_witness_spec_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "SELECTED_REPRESENTABLE_WITNESS_SPEC_TARGET_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "SELECTED_REPRESENTABLE_WITNESS_SPEC_TARGET_2026_06_24"
    assert data["parent_status"] == "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_TARGET_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["semantic_spec"]["name"] == "selected_domain_representable_witness_spec"
    assert data["derived_targets"]["SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM"]["status"] == "closed_conditionally_by_selected_domain_representable_witness_spec"
    assert data["derived_targets"]["UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED"]["status"] == "closed_conditionally"
    assert data["derived_targets"]["UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL"]["status"] == "closed_conditionally_by_well_founded_induction"
    assert data["derived_targets"]["UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR"]["status"] == "closed_conditionally_by_choice_from_relation_total"
    assert data["derived_targets"]["unrestricted_terminal_closure"]["status"] == "blocked"
    assert data["weakest_missing_object"]["name"] == "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER"

    for token in [
        "BOUNDARY := not SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved",
        "BOUNDARY := not unrestricted_terminal_closure_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "selected_domain_representable_witness_spec",
        "SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM :=",
        "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED :=",
        "UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL :=",
        "UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR :=",
        "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved",
    ]:
        assert token in doc

    print("SELECTED_REPRESENTABLE_WITNESS_SPEC_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
