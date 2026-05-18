#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedClayBoundaryLock.lean"
doc = ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_CLAY_BOUNDARY_LOCK_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/finite_support_restricted_clay_boundary_lock_2026_05_18.json"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "import Chronos.Frontier.FiniteSupportRestrictedBoundaryLock",
    "inductive FiniteSupportRestrictedClayBoundaryStatus",
    "| frontier_open",
    "| restricted_boundary_locked",
    "structure FiniteSupportRestrictedClayBoundaryLock",
    "boundary_lock : FiniteSupportRestrictedBoundaryLock D",
    "status_locked",
    "theorem finite_support_restricted_clay_boundary_lock",
    "theorem FiniteSupportRestrictedClayBoundaryLock_from_UFEG",
    "FiniteSupportRestrictedBoundaryLock_from_UFEG D h",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in ["sorry", "admit", "axiom"]:
    if token in lean_text:
        raise SystemExit(f"forbidden Lean token present: {token}")

if data["status"] != "FINITE_SUPPORT_RESTRICTED_CLAY_BOUNDARY_LOCK_CLOSED_ONLY":
    raise SystemExit("wrong artifact status")

if data["lean_theorem"] != "FiniteSupportRestrictedClayBoundaryLock_from_UFEG":
    raise SystemExit("wrong Lean theorem marker")

for phrase in [
    "finite-support admissible restricted domain only",
    "restricted boundary-status lock only",
    "no unrestricted UniversalFiberEntropyGap",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay closure",
]:
    if phrase not in doc_text:
        raise SystemExit(f"missing boundary phrase in doc: {phrase}")
    if phrase not in data["boundary"]:
        raise SystemExit(f"missing boundary phrase in artifact: {phrase}")

print("Finite-support restricted Clay boundary lock verified.")
