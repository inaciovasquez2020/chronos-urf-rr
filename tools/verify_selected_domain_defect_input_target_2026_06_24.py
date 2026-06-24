#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "selected_domain_defect_input_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "SELECTED_DOMAIN_DEFECT_INPUT_TARGET_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "SELECTED_DOMAIN_DEFECT_INPUT_TARGET_2026_06_24"
    assert data["parent_status"] == "UNRESTRICTED_WITNESS_CARRIER_INPUT_TARGET_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["definitions"]["SelectedDomainDefect"]["kind"] == "input_carrier"
    assert data["definitions"]["defect_atoms"]["type"] == "W_unrestricted -> Finset SelectedDomainDefect"
    assert data["definitions"]["selected_domain_defect"]["definition"] == "selected_domain_defect(w) := (defect_atoms(w)).card"
    assert data["blocked_proof_targets"]["defect_zero_implies_selected_domain_representable"]["status"] == "blocked"
    assert data["blocked_proof_targets"]["defect_positive_has_terminal_repair"]["status"] == "blocked"
    assert data["weakest_missing_object"]["name"] == "SELECTED_DOMAIN_DEFECT_SEMANTIC_SPEC"

    for token in [
        "BOUNDARY := not defect_zero_implies_selected_domain_representable_proved",
        "BOUNDARY := not defect_positive_has_terminal_repair_proved",
        "BOUNDARY := not SELECTED_DOMAIN_DEFECT_BASIS_proved",
        "BOUNDARY := not unrestricted_terminal_closure_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "SelectedDomainDefect",
        "defect_atoms : W_unrestricted -> Finset SelectedDomainDefect",
        "selected_domain_defect(w) :=",
        "SelectedDomainDefect_zero_completeness_spec",
        "SelectedDomainDefect_positive_repair_spec",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved",
    ]:
        assert token in doc

    print("SELECTED_DOMAIN_DEFECT_INPUT_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
