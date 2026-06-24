#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "represents_terminal_preserves_discharge_semantics_rule_target_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_TARGET_2026_06_24.md"
data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
doc = DOC.read_text(encoding="utf-8")
assert data["artifact"] == "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_TARGET_2026_06_24"
assert data["parent_commit"] == "5b8f3e3c"
assert data["parent_target"] == "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL_TARGET_2026_06_24"
assert data["rule_target"]["name"] == "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE"
assert data["rule_target"]["status"] == "target"
assert data["weakest_missing_object"]["name"] == "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT"
assert "DISCHARGE_SEMANTICS_CONGRUENCE_UNDER_REPRESENTS_TERMINAL" in data["closes_if_proved"]
assert "unrestricted_terminal_closure_nonconditional" in data["blocked_until_proved"]
assert "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT_proved" in data["boundaries"]
assert "BOUNDARY := not REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved" in data["boundaries"]
assert "BOUNDARY := not final_closure_claim_proved" in data["boundaries"]
assert "REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE := target" in doc
assert "REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_DEFINITIONAL_ALIGNMENT" in doc
assert "discharge_semantics_selected(nf)" in doc
assert "discharge_semantics_unrestricted(w)" in doc
assert "BOUNDARY := ¬ REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_proved" in doc
print("REPRESENTS_TERMINAL_PRESERVES_DISCHARGE_SEMANTICS_RULE_TARGET_2026_06_24_OK")
