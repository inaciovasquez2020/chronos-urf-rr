#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LEAN_FILE = ROOT / "lean/Chronos/Frontier/KnownClosedCantorBoundaryDemo.lean"
ARTIFACT_FILE = ROOT / "artifacts/external_validation/known_closed_cantor_boundary_demo_2026_06_30.json"
WORKFLOW_FILE = ROOT / ".github/workflows/external-status-lock.yml"
STATUS_LOCK_FILE = ROOT / "scripts/verify_external_status_lock.py"

THEOREM = "known_closed_cantor_boundary_demo"
MATHLIB_ANCHOR = "Function.cantor_surjective"
CLASSIFICATION = "KNOWN_CLOSED_THEOREM_DEMO"
COMMAND = "python3 tools/verifier/verify_known_closed_cantor_boundary_demo.py"
STEP_NAME = "Verify known closed Cantor boundary demo"

FORBIDDEN_LEAN_TOKENS = ("sorry", "axiom", "opaque", "admit")

FORBIDDEN_CLAIM_SUBSTRINGS = (
    "P vs NP",
    "Chronos-RR",
    "gravity",
    "cosmology",
    "foundations-of-physics",
    "open problems",
    "efficiency without a defined baseline",
)

NEGATIVE_BOUNDARY_FALSE_KEYS = (
    "frontier_closure",
    "open_problem_solution",
    "physics_closure",
    "complexity_closure",
    "efficiency_claim_without_baseline",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(LEAN_FILE.exists(), f"MISSING_OBJECT := {LEAN_FILE.relative_to(ROOT)}")
    require(ARTIFACT_FILE.exists(), f"MISSING_OBJECT := {ARTIFACT_FILE.relative_to(ROOT)}")
    require(WORKFLOW_FILE.exists(), f"MISSING_OBJECT := {WORKFLOW_FILE.relative_to(ROOT)}")
    require(STATUS_LOCK_FILE.exists(), f"MISSING_OBJECT := {STATUS_LOCK_FILE.relative_to(ROOT)}")

    lean_text = LEAN_FILE.read_text(encoding="utf-8")
    require(THEOREM in lean_text, f"MISSING_OBJECT := Lean theorem {THEOREM}")
    require(MATHLIB_ANCHOR in lean_text, f"MISSING_OBJECT := Mathlib anchor {MATHLIB_ANCHOR}")

    for token in FORBIDDEN_LEAN_TOKENS:
        require(token not in lean_text, f"FORBIDDEN_LEAN_TOKEN := {token}")

    artifact = json.loads(ARTIFACT_FILE.read_text(encoding="utf-8"))
    require(artifact.get("classification") == CLASSIFICATION, "BAD_CLASSIFICATION")
    require(artifact.get("closed_theorem", {}).get("lean_symbol") == THEOREM, "BAD_LEAN_SYMBOL")
    require(artifact.get("closed_theorem", {}).get("mathlib_anchor") == MATHLIB_ANCHOR, "BAD_MATHLIB_ANCHOR")

    allowed_claims = "\n".join(artifact.get("allowed_claims", []))
    require("Lean-checked closed-theorem demo" in allowed_claims, "MISSING_ALLOWED_CLOSED_THEOREM_CLAIM")

    forbidden_claims = "\n".join(artifact.get("forbidden_claims", []))
    for substring in FORBIDDEN_CLAIM_SUBSTRINGS:
        require(substring in forbidden_claims, f"MISSING_FORBIDDEN_CLAIM_SUBSTRING := {substring}")

    negative_boundary = artifact.get("negative_boundary", {})
    for key in NEGATIVE_BOUNDARY_FALSE_KEYS:
        require(negative_boundary.get(key) is False, f"BAD_NEGATIVE_BOUNDARY_FLAG := {key}")

    workflow_text = WORKFLOW_FILE.read_text(encoding="utf-8")
    status_lock_text = STATUS_LOCK_FILE.read_text(encoding="utf-8")
    require(STEP_NAME in workflow_text, f"MISSING_WORKFLOW_STEP := {STEP_NAME}")
    require(COMMAND in workflow_text, f"MISSING_WORKFLOW_COMMAND := {COMMAND}")
    require(STEP_NAME in status_lock_text, f"MISSING_STATUS_LOCK_STEP := {STEP_NAME}")
    require(COMMAND in status_lock_text, f"MISSING_STATUS_LOCK_COMMAND := {COMMAND}")

    print("KNOWN_CLOSED_CANTOR_BOUNDARY_DEMO_OK")


if __name__ == "__main__":
    main()
