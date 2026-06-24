#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "represents_terminal_discharge_semantics_definitional_alignment_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_TARGET_2026_06_24.md"

data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
doc = DOC.read_text(encoding="utf-8")

assert data["artifact"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_TARGET_2026_06_24"
assert data["parent_commit"] == "adcf7405"
assert data["parent_target"] == "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_TARGET_2026_06_24"
assert data["alignment_target"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT"
assert data["alignment_target"]["status"] == "target"
assert data["weakest_missing_object"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD"
assert "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE" in data["closes_if_proved"]
assert "DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally" in data["closes_if_proved"]

for token in [
    "selected representative terminal semantics",
    "unrestricted terminal witness semantics",
    "discharge semantics equality",
    "representation relation compatibility",
]:
    assert token in data["required_alignment_fields"]

for token in [
    "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_proved",
    "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved",
    "BOUNDARY := not REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved",
    "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
    "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
    "BOUNDARY := not final_closure_claim_proved",
]:
    assert token in data["boundaries"]

for token in [
    "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT := target",
    "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD",
    "discharge_semantics_selected(nf) = discharge_semantics_unrestricted(w)",
    "BOUNDARY := ¬ REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved",
]:
    assert token in doc

print("REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_TARGET_2026_06_24_OK")
