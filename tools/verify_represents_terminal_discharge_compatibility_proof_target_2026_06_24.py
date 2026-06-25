#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "represents_terminal_discharge_compatibility_proof_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_TARGET_2026_06_24.md"

def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["artifact"] == "REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_TARGET_2026_06_24"
    assert data["parent_commit"] == "3b696cd6"
    assert data["parent_target"] == "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_SPEC_SURFACE_2026_06_24"
    assert data["proof_target"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF"
    assert data["proof_target"]["status"] == "target"
    assert data["weakest_missing_object"]["name"] == "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL"

    obligation_names = {item["name"] for item in data["bounded_proof_obligations"]}
    assert "REPRESENTS_TERMINAL_DOMAIN_ALIGNMENT" in obligation_names
    assert "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL" in obligation_names
    assert "SELECTED_UNRESTRICTED_TERMINAL_DISCHARGE_EQUIVALENCE" in obligation_names

    for token in [
        "BOUNDARY := not DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_proved",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_proved",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF := target",
        "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL",
        "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)",
        "represents_terminal(nf,w)",
        "BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_proved",
    ]:
        assert token in doc

    print("REPRESENTS_TERMINAL_DISCHARGE_COMPATIBILITY_PROOF_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
