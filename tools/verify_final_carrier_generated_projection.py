#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/FinalCarrierGeneratedProjection.lean"
CHRONOS = ROOT / "Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/final_carrier_generated_projection_2026_05_12.json"
STATUS = ROOT / "docs/status/CHRONOS_FINAL_CARRIER_GENERATED_PROJECTION_2026_05_12.md"

for p in [LEAN, CHRONOS, ARTIFACT, STATUS]:
    if not p.exists():
        raise SystemExit(f"missing required file: {p.relative_to(ROOT)}")

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
status = STATUS.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessFromFintype",
    "theorem FinalCarrierDomain_repository_native_generated_from_finite_registry_exhaustiveness",
    "RepositoryNativeGenerated c",
    "rcases RepositoryNativeFiniteRegistryExhaustiveness with ⟨R, hR⟩",
    "exact (hR c hc).2",
    "theorem RepositoryNativeFiniteRegistryExhaustiveness_from_projected_generation",
    "RepositoryNativeFiniteRegistryExhaustiveness_from_fintype",
    "FinalCarrierDomain_repository_native_generated_from_finite_registry_exhaustiveness",
]

missing_lean = [tok for tok in required_lean_tokens if tok not in lean]
if missing_lean:
    raise SystemExit(f"missing Lean tokens: {missing_lean}")

if "import Chronos.Frontier.FinalCarrierGeneratedProjection" not in chronos:
    raise SystemExit("Chronos.lean does not import FinalCarrierGeneratedProjection")

if artifact.get("status") != "PROJECTION_ONLY":
    raise SystemExit("artifact status must remain PROJECTION_ONLY")

if artifact.get("theorem_level_closure") is not False:
    raise SystemExit("artifact theorem_level_closure must be false")

if artifact.get("weakest_missing_object") != "RepositoryNativeFiniteRegistryExhaustiveness":
    raise SystemExit("weakest missing object changed")

required_status_tokens = [
    "PROJECTION_ONLY",
    "Closed projection",
    "Source axiom",
    "Weakest missing object",
    "This is projection only.",
    "This does not prove RepositoryNativeFiniteRegistryExhaustiveness.",
    "This does not prove FinalCarrierDomain_repository_native_generated independently.",
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
    "RepositoryNativeFiniteRegistryExhaustiveness is proved",
    "FinalCarrierDomain_repository_native_generated independently proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is proved",
    "P vs NP is proved",
]:
    if forbidden in lean or forbidden in status:
        raise SystemExit(f"forbidden overclaim token present: {forbidden}")

print("Final carrier generated projection verified.")
