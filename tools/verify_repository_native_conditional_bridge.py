#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "chronos/Frontier/RepositoryNativeConditionalBridge.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_conditional_bridge_2026_05_07.json"
STATUS = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_CONDITIONAL_BRIDGE_2026_05_07.md"

required_lean_tokens = [
    "namespace Chronos.Frontier.RepositoryNativeConditionalBridge",
    "structure BridgeCarrier",
    "def SearchRecover",
    "def RecoveryLocalized",
    "structure SearchSolver",
    "structure RecoverySolver",
    "def InducedRecoverySolver",
    "structure ConditionalBridgeContract",
    "def RecoveryLowerBound",
    "def SearchLowerBound",
    "theorem ConditionalBridgeClaritySolved",
    "def C_Chronos",
    "theorem chronos_recovery_localized",
    "theorem chronos_conditional_bridge_instantiated",
    "end Chronos.Frontier.RepositoryNativeConditionalBridge",
]

required_status_tokens = [
    "Status: FRONTIER_OPEN",
    "Contract: CONDITIONAL_BRIDGE_CONTRACT",
    "chronos_recovery_localized_native",
    "No H4.1 closure.",
    "No FGL closure.",
    "No Chronos theorem-level closure.",
    "No P vs NP closure.",
    "No theorem-level Chronos lower bound is asserted.",
]

for path in [LEAN, ARTIFACT, STATUS]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")

lean_text = LEAN.read_text()
status_text = STATUS.read_text()
artifact = json.loads(ARTIFACT.read_text())

for token in required_lean_tokens:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "axiom", "admit"]:
    if re.search(rf"\b{forbidden}\b", lean_text):
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

for token in required_status_tokens:
    if token not in status_text:
        raise SystemExit(f"missing status token: {token}")

if artifact.get("status") != "FRONTIER_OPEN":
    raise SystemExit("artifact status must remain FRONTIER_OPEN")

if artifact.get("contract") != "CONDITIONAL_BRIDGE_CONTRACT":
    raise SystemExit("artifact contract must remain CONDITIONAL_BRIDGE_CONTRACT")

if artifact.get("theorem_closure") is not False:
    raise SystemExit("artifact theorem_closure must be false")

if artifact.get("remaining_frontier_object") != "chronos_recovery_localized_native":
    raise SystemExit("remaining frontier object must be chronos_recovery_localized_native")

for phrase in [
    "H4.1 closure",
    "FGL closure",
    "Chronos theorem-level closure",
    "P vs NP closure",
]:
    if phrase not in artifact.get("forbidden_closures", []):
        raise SystemExit(f"missing forbidden closure marker: {phrase}")

print("Repository-native conditional bridge verified: FRONTIER_OPEN / CONDITIONAL_BRIDGE_CONTRACT")
