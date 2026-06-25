#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "represents_terminal_discharge_semantics_field_realization_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_TARGET_2026_06_24.md"

def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["artifact"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_TARGET_2026_06_24"
    assert data["parent_commit"] == "3727416b"
    assert data["parent_target"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_TARGET_2026_06_24"
    assert data["realization_target"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION"
    assert data["realization_target"]["status"] == "target"
    assert data["required_payload"]["input"] == "represents_terminal(nf,w)"
    assert data["required_payload"]["output"] == "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)"
    assert data["weakest_missing_object"]["name"] == "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE"

    for token in [
        "field on a represents_terminal structure",
        "lemma derived from the represents_terminal definition",
        "definitional clause expanding represents_terminal",
        "adapter theorem from existing representation semantics",
    ]:
        assert token in data["acceptable_realizations"]

    for token in [
        "terminal_unrestricted(w)",
        "selected_domain(nf)",
        "terminal_T(nf)",
    ]:
        assert token in data["required_payload"]["side_conditions"]

    for token in [
        "BOUNDARY := not REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_identified",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_proved",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION := target",
        "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE",
        "input := represents_terminal(nf,w)",
        "output := discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)",
        "BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved",
    ]:
        assert token in doc

    print("REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
