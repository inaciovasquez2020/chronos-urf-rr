#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ArbitraryConcreteTargetRegistryComputation.lean"
ART = ROOT / "artifacts/chronos/arbitrary_concrete_target_registry_computation_2026_05_27.json"
DOC = ROOT / "docs/status/ARBITRARY_CONCRETE_TARGET_REGISTRY_COMPUTATION_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

required_lean_tokens = [
    "structure ConcreteTargetRegistry",
    "structure FiniteConcreteTargetRegistry",
    "structure OneRegistrySemanticComputation",
    "structure ArbitraryFiniteConcreteRegistryComputation",
    "def one_registry_computation_lifts_to_arbitrary_finite_concrete_target_registries",
    "def arbitraryConcreteTargetRegistryComputationBoundaryLock",
    "theorem arbitrary_concrete_target_registry_computation_boundary_locked",
]

for path in [LEAN, ART, DOC, ROOT_IMPORT]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = LEAN.read_text()
for token in required_lean_tokens:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

if "import Chronos.Frontier.ArbitraryConcreteTargetRegistryComputation" not in ROOT_IMPORT.read_text():
    raise SystemExit("missing Chronos.lean import")

data = json.loads(ART.read_text())
if data.get("status") != "FINITE_CONCRETE_TARGET_REGISTRY_COMPUTATION_LIFT_CLOSED_WITNESS_ONLY":
    raise SystemExit("incorrect status")

required_boundaries = {
    "arbitrary-registry computation without finite concrete target data",
    "canonical witness construction for every concrete target registry",
    "unrestricted semantic-rank-to-fiber-entropy bridge",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

actual_boundaries = set(data.get("does_not_prove", []))
missing = required_boundaries - actual_boundaries
if missing:
    raise SystemExit(f"missing artifact boundary entries: {sorted(missing)}")

doc_text = DOC.read_text()
for boundary in required_boundaries:
    if boundary not in doc_text:
        raise SystemExit(f"missing doc boundary: {boundary}")

for forbidden in [
    "unrestricted Chronos-RR closed",
    "unrestricted H4.1/FGL closed",
    "UniversalFiberEntropyGap closed",
    "P vs NP closed",
    "Clay problem solved",
]:
    if forbidden in lean_text or forbidden in ART.read_text() or forbidden in doc_text:
        raise SystemExit(f"forbidden overclaim token present: {forbidden}")

print("ARBITRARY_CONCRETE_TARGET_REGISTRY_COMPUTATION_OK")
