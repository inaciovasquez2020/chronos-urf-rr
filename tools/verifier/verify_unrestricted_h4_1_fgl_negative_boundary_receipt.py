#!/usr/bin/env python3
import json
import sys
from pathlib import Path

EXPECTED_PERCENTAGE = 85
TRACKED_FILE = Path("Chronos/Frontier/H4_1_FGL_FinalSelectedInputClosure.lean")
ARTIFACT_FILE = Path("artifacts/external_validation/restricted_package_theorem_surface_boundary_2026_06_30.json")

def fail(message: str) -> None:
    raise SystemExit(f"UNRESTRICTED_H4_1_FGL_NEGATIVE_BOUNDARY_RECEIPT_FAIL := {message}")

def main() -> None:
    if not TRACKED_FILE.exists():
        fail(f"missing tracked file {TRACKED_FILE}")

    content = TRACKED_FILE.read_text(encoding="utf-8")

    required_fragments = [
        "def unrestricted_h4_1_fgl_closed : Prop :=",
        "theorem unrestricted_h4_1_fgl_promotion_refuted :",
        "¬ unrestricted_h4_1_fgl_closed := by",
        "H4_1_FGL_arbitrary_semantic_final_carrier_separating_observable_refuted",
    ]

    for fragment in required_fragments:
        if fragment not in content:
            fail(f"missing Lean fragment: {fragment}")

    forbidden_affirmations = [
        "theorem unrestricted_h4_1_fgl_closed_proof",
        "theorem unrestricted_h4_1_fgl_proven",
    ]

    for claim in forbidden_affirmations:
        if claim in content:
            fail(f"forbidden affirmative claim found: {claim}")

    if not ARTIFACT_FILE.exists():
        fail(f"missing artifact file {ARTIFACT_FILE}")

    data = json.loads(ARTIFACT_FILE.read_text(encoding="utf-8"))

    pct = data.get("metrics", {}).get("unrestricted_program_completion_pct")
    if pct != EXPECTED_PERCENTAGE:
        fail(f"completion metric mismatch: expected {EXPECTED_PERCENTAGE}, got {pct}")

    if data.get("unrestricted_domain_status") != "REFUTED_OPEN_GAP":
        fail("unrestricted_domain_status must be REFUTED_OPEN_GAP")

    print("UNRESTRICTED_H4_1_FGL_NEGATIVE_BOUNDARY_RECEIPT_OK")

if __name__ == "__main__":
    main()
