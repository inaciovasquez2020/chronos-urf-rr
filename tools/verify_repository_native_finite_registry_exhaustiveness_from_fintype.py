#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/RepositoryNativeFiniteRegistryExhaustivenessFromFintype.lean"
CHRONOS = ROOT / "Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_finite_registry_exhaustiveness_from_fintype.json"
STATUS = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_FINITE_REGISTRY_EXHAUSTIVENESS_FROM_FINTYPE_2026_05_12.md"

for p in [LEAN, CHRONOS, ARTIFACT, STATUS]:
    if not p.exists():
        raise SystemExit(f"missing required file: {p.relative_to(ROOT)}")

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
status = STATUS.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessBridge",
    "theorem RepositoryNativeFiniteRegistryExhaustiveness_from_fintype",
    "[Fintype { c : ChronosCarrierData // FinalCarrierDomain c }]",
    "FinalCarrierDomain c →",
    "RepositoryNativeGenerated c",
    "Finset.univ.image Subtype.val",
    "Finset.mem_image.mpr ⟨⟨c, hc⟩, Finset.mem_univ _, rfl⟩",
    "axiom FinalCarrierDomain_fintype",
    "theorem FinalCarrierDomain_repository_native_generated",
    "theorem RepositoryNativeFiniteRegistryExhaustiveness_from_fintype_axioms",
]

missing_lean = [tok for tok in required_lean_tokens if tok not in lean]
if missing_lean:
    raise SystemExit(f"missing Lean tokens: {missing_lean}")

if "import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessFromFintype" not in chronos:
    raise SystemExit("Chronos.lean does not import the fintype reduction module")

if artifact.get("status") != "CONDITIONAL_REDUCTION_ONLY":
    raise SystemExit("artifact status must remain CONDITIONAL_REDUCTION_ONLY")

if artifact.get("theorem_level_closure") is not False:
    raise SystemExit("artifact theorem_level_closure must be false")

if artifact.get("weakest_missing_object") != "FinalCarrierDomain_repository_native_generated":
    raise SystemExit("weakest missing object changed")

required_status_tokens = [
    "CONDITIONAL_REDUCTION_ONLY",
    "Weakest missing object",
    "This does not prove FinalCarrierDomain_repository_native_generated.",
    "This does not prove RepositoryNativeFiniteRegistryExhaustiveness unconditionally.",
    "This does not prove unconditional UniversalFiberEntropyGap.",
    "This does not prove broader DepthBridge.",
    "This does not prove Chronos-RR.",
    "This does not prove H4.1/FGL.",
    "This does not prove P vs NP.",
    "This does not prove any Clay-problem closure.",
]

missing_status = [tok for tok in required_status_tokens if tok not in status]
if missing_status:
    raise SystemExit(f"missing status tokens: {missing_status}")

for forbidden in [
    "FinalCarrierDomain_repository_native_generated is proved",
    "RepositoryNativeFiniteRegistryExhaustiveness is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is proved",
    "P vs NP is proved",
]:
    if forbidden in lean or forbidden in status:
        raise SystemExit(f"forbidden overclaim token present: {forbidden}")

print("Repository-native finite registry exhaustiveness from fintype verified.")
