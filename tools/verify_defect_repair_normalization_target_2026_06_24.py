#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "defect_repair_normalization_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "DEFECT_REPAIR_NORMALIZATION_TARGET_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "DEFECT_REPAIR_NORMALIZATION_TARGET_2026_06_24"
    assert data["parent_status"] == "SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["repair_descent_spec"]["name"] == "defect_repair_decreases_selected_domain_defect"
    assert data["repair_descent_spec"]["status"] == "closed_conditionally_by_repair_descent_spec"
    assert data["derived_targets"]["UNRESTRICTED_TERMINAL_NORMALIZATION_STEP_RULE"]["status"] == "closed_conditionally"
    assert data["derived_targets"]["UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL"]["first_missing_object"] == "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED"
    assert data["weakest_missing_object"]["name"] == "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED"

    for token in [
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_proved",
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved",
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMAL_FORM_CONSTRUCTOR_defined",
        "BOUNDARY := not unrestricted_terminal_closure_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "defect_repair_decreases_selected_domain_defect",
        "UNRESTRICTED_TERMINAL_NORMALIZATION_STEP_RULE :=",
        "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved",
    ]:
        assert token in doc

    print("DEFECT_REPAIR_NORMALIZATION_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
