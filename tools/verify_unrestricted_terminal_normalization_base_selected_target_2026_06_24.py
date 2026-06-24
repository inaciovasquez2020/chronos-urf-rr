#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "unrestricted_terminal_normalization_base_selected_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_TARGET_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_TARGET_2026_06_24"
    assert data["parent_status"] == "DEFECT_REPAIR_NORMALIZATION_TARGET_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["target"]["name"] == "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED"
    assert data["target"]["status"] == "blocked"
    assert data["first_usable_input"]["name"] == "defect_zero_implies_selected_domain_representable"
    assert data["weakest_missing_object"]["name"] == "SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM"

    for token in [
        "BOUNDARY := not SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM_proved",
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_proved",
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved",
        "BOUNDARY := not unrestricted_terminal_closure_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED",
        "defect_zero_implies_selected_domain_representable",
        "SELECTED_REPRESENTABLE_HAS_TERMINAL_NORMAL_FORM",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved",
    ]:
        assert token in doc

    print("UNRESTRICTED_TERMINAL_NORMALIZATION_BASE_SELECTED_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
