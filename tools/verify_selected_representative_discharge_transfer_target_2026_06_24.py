#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "selected_representative_discharge_transfer_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_TARGET_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_TARGET_2026_06_24"
    assert data["parent_status"] == "SELECTED_REPRESENTABLE_WITNESS_SPEC_TARGET_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["transfer_spec"]["name"] == "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER"
    assert data["derived_targets"]["A7k_TERMINAL_CLOSURE_selected_applied_to_nf"]["status"] == "available"
    assert data["derived_targets"]["discharged_T_nf_to_discharged_unrestricted_w"]["status"] == "closed_conditionally_by_SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER"
    assert data["derived_targets"]["unrestricted_terminal_closure"]["status"] == "conditional"
    assert data["boundary"]["final_closure_claim"] == "stopped"
    assert data["weakest_missing_object"]["name"] == "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE"

    for token in [
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved",
        "BOUNDARY := not SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
    ]:
        assert token in data["boundaries"]

    for token in [
        "SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER",
        "A7k_TERMINAL_CLOSURE_selected applied to nf",
        "unrestricted_terminal_closure :=",
        "conditional on SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER",
        "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE",
        "BOUNDARY := ¬ unrestricted_terminal_closure_proved_nonconditionally",
    ]:
        assert token in doc

    print("SELECTED_REPRESENTATIVE_DISCHARGE_TRANSFER_TARGET_2026_06_24_OK")

if __name__ == "__main__":
    main()
