#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/RestrictedChronosRRToRestrictedH41FGL.lean"
doc = ROOT / "docs/status/RESTRICTED_CHRONOS_RR_TO_RESTRICTED_H41FGL_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/restricted_chronos_rr_to_restricted_h41_fgl_2026_05_18.json"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure RestrictedChronosRRData",
    "abbrev RestrictedChronosRR",
    "abbrev RestrictedH41FGL",
    "theorem restricted_h41_fgl_from_restricted_chronos_rr",
    "theorem restricted_chronos_rr_to_restricted_h41_fgl",
    "theorem RestrictedChronosRRToRestrictedH41FGL",
    "RestrictedChronosRR D → RestrictedH41FGL D",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in ["sorry", "admit", "axiom"]:
    if token in lean_text:
        raise SystemExit(f"forbidden Lean token present: {token}")

if data["status"] != "RESTRICTED_H41FGL_TARGET_CLOSED_ONLY":
    raise SystemExit("wrong artifact status")

if data["lean_theorem"] != "RestrictedChronosRRToRestrictedH41FGL":
    raise SystemExit("wrong Lean theorem marker")

for phrase in [
    "finite-support admissible restricted domain only",
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

print("Restricted Chronos-RR to restricted H4.1/FGL verified.")
