#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "discharge_semantics_congruence_under_represents_terminal_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_TARGET_2026_06_24.md"

def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["artifact"] == "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_TARGET_2026_06_24"
    assert data["parent_commit"] == "a6930247"
    assert data["parent_target"] == "REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_TARGET_2026_06_24"
    assert data["lemma_target"]["name"] == "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL"
    assert data["lemma_target"]["status"] == "target"
    assert data["output_conclusion"] == "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)"
    assert data["weakest_missing_object"]["name"] == "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE"

    for token in [
        "terminal_unrestricted(w)",
        "selected_domain(nf)",
        "terminal_T(nf)",
        "represents_terminal(nf,w)",
    ]:
        assert token in data["input_hypotheses"]

    for token in [
        "BOUNDARY := not REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved",
        "BOUNDARY := not DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_proved",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_proved",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL := target",
        "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)",
        "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE",
        "BOUNDARY := ¬ DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_proved",
    ]:
        assert token in doc

    print("DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
