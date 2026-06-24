#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/selected_domain_stack_final_conditional_review_2026_06_24.json")
DOC = Path("docs/status/SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24.md")

artifact = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()

assert artifact["id"] == "SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24"
assert artifact["target_branch"] == "docs/selected-domain-defect-basis-2026-06-24"
assert artifact["merge_commit"] == "603dc138"
assert artifact["source_head"] == "e03cc74f"
assert artifact["conditional_selected_domain_stack"] == "merged"
assert artifact["unconditional_oblivion_closure"] == "not solved"
assert artifact["boundary"] == "preserved"
assert artifact["main_decision"] == "do not merge to main yet"
assert artifact["weakest_missing_object"] == "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed"
assert artifact["status"] == "final_conditional_selected_domain_stack_review_recorded"

branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
assert branch == artifact["target_branch"]

head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
assert head == artifact["merge_commit"]

subprocess.run(["git", "merge-base", "--is-ancestor", artifact["source_head"], "HEAD"], check=True)

required_doc_tokens = [
    "SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24_OK",
    "CONDITIONAL_SELECTED_DOMAIN_STACK := merged",
    "UNCONDITIONAL_OBLIVION_CLOSURE := not solved",
    "BOUNDARY := preserved",
    "Do not merge to main yet.",
    "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved",
    "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed",
]
for token in required_doc_tokens:
    assert token in doc

required_paths = [
    "lean/Chronos/Frontier/SelectedDomainUnconditionalClosureConstructorObligationMatrix.lean",
    "docs/status/SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_MERGE_READINESS_2026_06_24.md",
    "tools/verify_selected_domain_defect_repair_interface_merge_readiness_2026_06_24.py",
    "tests/test_selected_domain_defect_repair_interface_merge_readiness_2026_06_24.py",
]
for path in required_paths:
    assert Path(path).exists(), path

print("SELECTED_DOMAIN_STACK_FINAL_CONDITIONAL_REVIEW_2026_06_24_OK")
