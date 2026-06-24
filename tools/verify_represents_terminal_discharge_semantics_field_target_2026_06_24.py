#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "represents_terminal_discharge_semantics_field_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_TARGET_2026_06_24.md"

def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["artifact"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_TARGET_2026_06_24"
    assert data["parent_commit"] == "8f7d1c34"
    assert data["parent_target"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_TARGET_2026_06_24"
    assert data["field_target"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD"
    assert data["field_target"]["status"] == "target"
    assert data["required_field_contract"]["input_relation"] == "represents_terminal(nf,w)"
    assert data["required_field_contract"]["required_equality"] == "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)"
    assert data["weakest_missing_object"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION"

    for token in [
        "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT",
        "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE",
        "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL",
        "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
    ]:
        assert token in data["closes_if_realized"]

    for token in [
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_proved",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD := target",
        "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION",
        "input_relation := represents_terminal(nf,w)",
        "required_equality := discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)",
        "BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_proved",
    ]:
        assert token in doc

    print("REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
