#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/RepositoryNativeFiniteRegistryExhaustivenessIndependent.lean"
CHRONOS = ROOT / "Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_finite_registry_exhaustiveness_independent_2026_05_12.json"
STATUS = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_FINITE_REGISTRY_EXHAUSTIVENESS_INDEPENDENT_2026_05_12.md"

for p in [LEAN, CHRONOS, ARTIFACT, STATUS]:
    if not p.exists():
        raise SystemExit(f"missing required file: {p.relative_to(ROOT)}")

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
status = STATUS.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "theorem FinalCarrierDomain_repository_native_generated_independent",
    "FinalCarrierDomain c →",
    "RepositoryNativeGenerated c",
    "positive_arity_repository_native_image_covers c",
    "simpa [FinalCarrierDomain] using hc",
    "theorem RepositoryNativeFiniteRegistryExhaustiveness_independent",
    "letI := FinalCarrierDomain_fintype",
    "RepositoryNativeFiniteRegistryExhaustiveness_from_fintype",
    "FinalCarrierDomain_repository_native_generated_independent",
]

missing_lean = [tok for tok in required_lean_tokens if tok not in lean]
if missing_lean:
    raise SystemExit(f"missing Lean tokens: {missing_lean}")

for forbidden in [
    "rcases RepositoryNativeFiniteRegistryExhaustiveness with",
    "exact RepositoryNativeFiniteRegistryExhaustiveness\n",
    "exact RepositoryNativeFiniteRegistryExhaustiveness ",
    "RepositoryNativeFiniteRegistryExhaustiveness := by",
]:
    if forbidden in lean:
        raise SystemExit(f"forbidden circular dependency present: {forbidden}")

if "import Chronos.Frontier.RepositoryNativeFiniteRegistryExhaustivenessIndependent" not in chronos:
    raise SystemExit("Chronos.lean does not import the independent reduction module")

if artifact.get("status") != "INDEPENDENT_REDUCTION_WITH_FINITE_DOMAIN_AXIOM":
    raise SystemExit("artifact status changed")

if artifact.get("remaining_axiom") != "FinalCarrierDomain_fintype":
    raise SystemExit("remaining axiom must be FinalCarrierDomain_fintype")

if artifact.get("theorem_level_closure") is not False:
    raise SystemExit("theorem_level_closure must be false")

required_status_tokens = [
    "INDEPENDENT_REDUCTION_WITH_FINITE_DOMAIN_AXIOM",
    "Closed independent generation",
    "Remaining finite-domain axiom",
    "This does not use RepositoryNativeFiniteRegistryExhaustiveness.",
    "This uses FinalCarrierDomain_fintype.",
    "This does not prove finite-domain closure from raw constructors.",
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

print("Independent finite registry exhaustiveness reduction verified.")
