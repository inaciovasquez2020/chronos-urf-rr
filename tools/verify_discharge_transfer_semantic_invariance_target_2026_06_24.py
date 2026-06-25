#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "discharge_transfer_semantic_invariance_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_TARGET_2026_06_24.md"

def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["artifact"] == "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_TARGET_2026_06_24"
    assert data["parent_commit"] == "37c9a9a0"
    assert data["target"]["name"] == "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE"
    assert data["target"]["status"] == "target"
    assert data["weakest_missing_object"]["name"] == "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE"
    assert data["current_boundary"]["unrestricted_terminal_closure"] == "conditional"
    assert data["current_boundary"]["final_closure_claim"] == "stopped"

    for token in [
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved",
        "BOUNDARY := not SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundaries"]

    for token in [
        "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE",
        "represents_terminal(nf,w) preserves discharge semantics",
        "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_nonconditional := blocked",
        "unrestricted_terminal_closure_nonconditional := blocked",
        "final_closure_claim := stopped",
        "BOUNDARY := ¬ DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved",
    ]:
        assert token in doc

    print("DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
