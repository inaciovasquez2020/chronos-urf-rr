#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedUFEGToRestrictedH41FGL.lean"
doc = ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_H41FGL_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/finite_support_restricted_ufeg_to_restricted_h41_fgl_2026_05_18.json"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "import Chronos.Frontier.RestrictedChronosRRToRestrictedH41FGL",
    "structure FiniteSupportRestrictedUFEGToRestrictedH41FGLData",
    "def toRestrictedChronosRRData",
    "abbrev FiniteSupportRestrictedUFEG",
    "abbrev FiniteSupportRestrictedH41FGL",
    "theorem finite_support_restricted_ufeg_to_restricted_chronos_rr",
    "theorem finite_support_restricted_ufeg_to_restricted_h41_fgl",
    "theorem FiniteSupportRestrictedUFEGToRestrictedH41FGL",
    "RestrictedChronosRRToRestrictedH41FGL",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in ["sorry", "admit", "axiom"]:
    if token in lean_text:
        raise SystemExit(f"forbidden Lean token present: {token}")

if data["status"] != "FINITE_SUPPORT_RESTRICTED_H41FGL_TARGET_CLOSED_ONLY":
    raise SystemExit("wrong artifact status")

if data["lean_theorem"] != "FiniteSupportRestrictedUFEGToRestrictedH41FGL":
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

print("Finite-support restricted UFEG to restricted H4.1/FGL verified.")
