#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "represents_terminal_semantic_payload_source_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_TARGET_2026_06_24.md"

def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["artifact"] == "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_TARGET_2026_06_24"
    assert data["parent_commit"] == "18e22c41"
    assert data["parent_target"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_TARGET_2026_06_24"
    assert data["source_target"]["name"] == "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE"
    assert data["source_target"]["status"] == "target"
    assert data["required_payload"]["relation"] == "represents_terminal(nf,w)"
    assert data["required_payload"]["required_equality"] == "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)"
    assert data["weakest_missing_object"]["name"] == "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION"

    for token in [
        "existing represents_terminal structure field",
        "existing lemma about represents_terminal semantic equality",
        "new minimal definitional clause on represents_terminal",
        "adapter lemma from representation semantics to discharge semantics equality",
    ]:
        assert token in data["admissible_source_forms"]

    for token in [
        "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION",
        "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE",
        "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL",
        "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
    ]:
        assert token in data["closes_if_identified"]

    for token in [
        "BOUNDARY := not REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION_identified",
        "BOUNDARY := not REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_identified",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE := target",
        "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION",
        "relation := represents_terminal(nf,w)",
        "required_equality := discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)",
        "BOUNDARY := ¬ REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_identified",
    ]:
        assert token in doc

    print("REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
