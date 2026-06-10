#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/RepositoryNativeFiniteRegistryExhaustivenessBridge.lean"
CHRONOS = ROOT / "Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_finite_registry_exhaustiveness_bridge.json"
STATUS = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_FINITE_REGISTRY_EXHAUSTIVENESS_BRIDGE_2026_05_12.md"

required_lean_tokens = [
    "def RepositoryNativeFiniteRegistryExhaustiveness",
    "∃ R : Finset ChronosCarrierData",
    "FinalCarrierDomain c →",
    "c ∈ R ∧ RepositoryNativeGenerated c",
    "theorem FinalCarrierGeneratedByFiniteRegistry_from_toolkit",
    "RepositoryNativeGenerated c ∧ c ∈ R",
    "rcases RepositoryNativeFiniteRegistryExhaustiveness with ⟨R, hR⟩",
    "exact ⟨(hR c hc).2, (hR c hc).1⟩",
    "theorem UniversalFiberEntropyGap_from_toolkit_registry",
    "UniversalFiberEntropyGap_from_finite_registry_generation hNF",
]

required_status_tokens = [
    "CONDITIONAL_BRIDGE_ONLY",
    "Weakest missing object",
    "This does not prove RepositoryNativeFiniteRegistryExhaustiveness.",
    "This does not prove unconditional UniversalFiberEntropyGap.",
    "This does not prove broader DepthBridge.",
    "This does not prove Chronos-RR.",
    "This does not prove H4.1/FGL.",
    "This does not prove P vs NP.",
    "This does not prove any Clay-problem closure.",
]

for p in [LEAN, CHRONOS, ARTIFACT, STATUS]:
    if not p.exists():
        raise SystemExit(f"missing required file: {p.relative_to(ROOT)}")

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
status = STATUS.read_text()
artifact = json.loads(ARTIFACT.read_text())

missing_lean = [tok for tok in required_lean_tokens if tok not in lean]
if missing_lean:
    raise SystemExit(f"missing Lean tokens: {missing_lean}")

import_line = "import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessBridge"
if import_line not in chronos:
    raise SystemExit("Chronos.lean does not import the bridge module")

missing_status = [tok for tok in required_status_tokens if tok not in status]
if missing_status:
    raise SystemExit(f"missing status tokens: {missing_status}")

if artifact.get("status") != "CONDITIONAL_BRIDGE_ONLY":
    raise SystemExit("artifact status must remain CONDITIONAL_BRIDGE_ONLY")

if artifact.get("theorem_level_closure") is not False:
    raise SystemExit("artifact theorem_level_closure must be false")

if artifact.get("weakest_missing_object") != "RepositoryNativeFiniteRegistryExhaustiveness":
    raise SystemExit("weakest missing object changed")

for forbidden in [
    "unconditional Chronos-RR",
    "Chronos-RR is proved",
    "P vs NP is proved",
    "RepositoryNativeFiniteRegistryExhaustiveness is proved",
]:
    if forbidden in lean or forbidden in status:
        raise SystemExit(f"forbidden overclaim token present: {forbidden}")

print("Repository-native finite registry exhaustiveness bridge verified.")
