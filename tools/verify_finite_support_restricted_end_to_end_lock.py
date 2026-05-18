#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedEndToEndLock.lean"
doc = ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_END_TO_END_LOCK_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/finite_support_restricted_end_to_end_lock_2026_05_18.json"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "import Chronos.Frontier.FiniteSupportRestrictedUFEGToRestrictedH41FGL",
    "theorem finite_support_restricted_end_to_end_h41_fgl",
    "theorem FiniteSupportRestrictedEndToEndH41FGL",
    "FiniteSupportRestrictedUFEG D → FiniteSupportRestrictedH41FGL D",
    "FiniteSupportRestrictedUFEGToRestrictedH41FGL D",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in ["sorry", "admit", "axiom"]:
    if token in lean_text:
        raise SystemExit(f"forbidden Lean token present: {token}")

if data["status"] != "FINITE_SUPPORT_RESTRICTED_END_TO_END_LOCK_CLOSED_ONLY":
    raise SystemExit("wrong artifact status")

if data["lean_theorem"] != "FiniteSupportRestrictedEndToEndH41FGL":
    raise SystemExit("wrong Lean theorem marker")

for phrase in [
    "finite-support admissible restricted domain only",
    "assembly lock only",
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

print("Finite-support restricted end-to-end H4.1/FGL lock verified.")
