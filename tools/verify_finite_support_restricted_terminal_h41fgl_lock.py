#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedTerminalH41FGLLock.lean"
doc = ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_TERMINAL_H41FGL_LOCK_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/finite_support_restricted_terminal_h41fgl_lock_2026_05_18.json"

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "import Chronos.Frontier.FiniteSupportRestrictedEndToEndLock",
    "structure FiniteSupportRestrictedTerminalH41FGLLock",
    "restricted_h41_fgl : FiniteSupportRestrictedH41FGL D",
    "theorem finite_support_restricted_terminal_h41fgl_lock",
    "theorem FiniteSupportRestrictedTerminalH41FGLLock_from_UFEG",
    "FiniteSupportRestrictedEndToEndH41FGL D h",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in ["sorry", "admit", "axiom"]:
    if token in lean_text:
        raise SystemExit(f"forbidden Lean token present: {token}")

if data["status"] != "FINITE_SUPPORT_RESTRICTED_TERMINAL_H41FGL_LOCK_CLOSED_ONLY":
    raise SystemExit("wrong artifact status")

if data["lean_theorem"] != "FiniteSupportRestrictedTerminalH41FGLLock_from_UFEG":
    raise SystemExit("wrong Lean theorem marker")

for phrase in [
    "finite-support admissible restricted domain only",
    "terminal restricted surface only",
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

print("Finite-support restricted terminal H4.1/FGL lock verified.")
