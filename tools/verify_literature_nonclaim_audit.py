#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "external_validation"

FORBIDDEN_PATTERNS = [
    r"\bsolve[sd]?\s+gravity\b",
    r"\bgravity\s+(is\s+)?solve[sd]\b",
    r"\bexperimental(?:ly)?\s+validat(?:ed|ion)\b",
    r"\bempirical(?:ly)?\s+validat(?:ed|ion)\b",
    r"\bEinstein(?:\s+field)?\s+equation(?:s)?\s+replacement\b",
    r"\breplace[sd]?\s+(?:the\s+)?Einstein(?:\s+field)?\s+equation(?:s)?\b",
    r"\bphysical\s+field\s+equation\b",
    r"\bexternal[- ]problem\s+closure\b",
    r"\bclosed\s+(?:an|the)?\s*external\s+problem\b",
    r"\baccepted\s+gravity\s+theory\b",
]

NONCLAIM_GUARDS = (
    "no_",
    "no ",
    "not ",
    "non-claim",
    "non_claim",
    "forbidden",
    "reject",
    "rejected",
    "preserved",
    "boundary",
    "does not",
    "must not",
    "missing ",
)

REQUIRED_NON_CLAIMS = {
    "no_gravity_solution_claim",
    "no_experimental_validation_claim",
    "no_einstein_equation_replacement_claim",
    "no_physical_field_equation_claim",
    "no_external_problem_closure_claim",
}

REFERENCE_KEYS = {
    "references",
    "literature_references",
    "methodology_references",
    "citations",
}

ROLE_VALUES = {
    "methodology",
    "background",
    "analogy",
    "context",
    "support_only",
}

NONCLAIM_METADATA_KEYS = {
    "boundary",
    "boundaries",
    "claim_boundaries",
    "does_not_claim",
    "does_not_support",
    "non_claim",
    "non_claims",
    "non_claims_preserved",
    "strict_non_claims",
    "forbidden_claims",
    "forbidden_phrases",
    "rejected_claims",
}

def walk_claim_strings(x, key=None):
    if key in NONCLAIM_METADATA_KEYS:
        return
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from walk_claim_strings(v, k)
    elif isinstance(x, list):
        for v in x:
            yield from walk_claim_strings(v, key)

def find_reference_lists(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if k in REFERENCE_KEYS and isinstance(v, list):
                yield k, v
            yield from find_reference_lists(v)
    elif isinstance(x, list):
        for v in x:
            yield from find_reference_lists(v)

def fail(path, reason):
    print(f"LITERATURE_NONCLAIM_AUDIT_FAIL := {path}")
    print(f"REASON := {reason}")
    raise SystemExit(1)

def audit_reference(path, ref):
    if not isinstance(ref, dict):
        fail(path, "reference entry is not an object")

    if ref.get("supports_only") is not True:
        fail(path, "reference missing supports_only := true")

    role = ref.get("reference_role")
    if role not in ROLE_VALUES:
        fail(path, f"reference_role must be one of {sorted(ROLE_VALUES)}")

    preserved = ref.get("non_claims_preserved")
    if not isinstance(preserved, list):
        fail(path, "non_claims_preserved must be a list")

    missing = REQUIRED_NON_CLAIMS.difference(set(preserved))
    if missing:
        fail(path, f"missing non_claims_preserved entries: {sorted(missing)}")

def audit_file(path):
    data = json.loads(path.read_text(encoding="utf-8"))

    for text in walk_claim_strings(data):
        lowered = text.lower()
        guarded = any(marker in lowered for marker in NONCLAIM_GUARDS)
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, text, flags=re.IGNORECASE) and not guarded:
                fail(path.relative_to(ROOT), f"forbidden claim phrase matched: {pat}")

    found_refs = False
    for _, refs in find_reference_lists(data):
        found_refs = True
        for ref in refs:
            audit_reference(path.relative_to(ROOT), ref)

    return found_refs

def main():
    if not ARTIFACT_DIR.is_dir():
        fail(ARTIFACT_DIR.relative_to(ROOT), "external validation artifact directory missing")

    json_paths = sorted(ARTIFACT_DIR.glob("*.json"))
    if not json_paths:
        fail(ARTIFACT_DIR.relative_to(ROOT), "no external validation JSON artifacts found")

    audited = 0
    for path in json_paths:
        if audit_file(path):
            audited += 1

    print("LITERATURE_NONCLAIM_AUDIT_OK")
    print(f"AUDITED_REFERENCE_ARTIFACTS := {audited}")

if __name__ == "__main__":
    main()
