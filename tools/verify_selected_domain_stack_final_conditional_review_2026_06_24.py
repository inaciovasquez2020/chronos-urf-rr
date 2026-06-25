#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_stack_final_conditional_review_2026_06_24.json")
DOC = Path("docs/status/SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24.md")

artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()

assert artifact["id"] == "SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"

required_tokens = [
    "SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24_OK",
    "CONDITIONAL_SELECTED_DOMAIN_STACK",
    "UNCONDITIONAL_OBLIVION_CLOSURE",
    "BOUNDARY",
]

for token in required_tokens:
    assert token in doc

assert "not solved" in doc
assert "preserved" in doc

print("SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24_OK")
