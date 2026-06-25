#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "selected_domain_defect_semantic_spec_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC_2026_06_24"
    assert data["parent_status"] == "SELECTED_DOMAIN_DEFECT_INPUT_TARGET_2026_06_24"
    assert data["executable_simulation"] is False
    assert "SelectedDomainDefect_zero_completeness_spec" in data["semantic_specs"]
    assert "SelectedDomainDefect_positive_repair_spec" in data["semantic_specs"]
    assert data["derived_targets"]["defect_zero_implies_selected_domain_representable"]["status"] == "closed_by_spec"
    assert data["derived_targets"]["defect_positive_has_terminal_repair"]["status"] == "closed_by_spec"
    assert data["derived_targets"]["SELECTED_DOMAIN_DEFECT_BASIS"]["status"] == "closed_conditionally_by_semantic_specs"
    assert data["remaining_blocker"]["name"] == "defect_repair_decreases_selected_domain_defect"

    for token in [
        "BOUNDARY := not defect_repair_decreases_selected_domain_defect_proved",
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMALIZATION_STEP_RULE_proved",
        "BOUNDARY := not UNRESTRICTED_TERMINAL_NORMALIZATION_RELATION_TOTAL_proved",
        "BOUNDARY := not unrestricted_terminal_closure_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "SelectedDomainDefect_zero_completeness_spec",
        "SelectedDomainDefect_positive_repair_spec",
        "defect_zero_implies_selected_domain_representable :=",
        "defect_positive_has_terminal_repair :=",
        "SELECTED_DOMAIN_DEFECT_BASIS :=",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved",
    ]:
        assert token in doc

    print("SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC_2026_06_24_OK")

if __name__ == "__main__":
    main()
