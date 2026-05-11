#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

LEAN_FILE = ROOT / "Chronos/Frontier/RepositoryNativeZeroArityCarrierMigrationTarget.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_zero_arity_carrier_migration_target_2026_05_11.json"
DOC = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_ZERO_ARITY_CARRIER_MIGRATION_TARGET_2026_05_11.md"

REQUIRED_LEAN_TOKENS = [
    "structure RepositoryNativeZeroArityInterface",
    "Carrier : Type",
    "Registry : Type",
    "arity : Carrier → Nat",
    "carrierRegistry : Carrier → Registry",
    "registryGenerates : Registry → Carrier → Prop",
    "finiteRegistry : Registry → Prop",
    "representedZeroArityRegistryPair : Carrier → Prop",
    "isFiniteRepresentedAtom : Carrier → Prop",
    "carrierRegistryGenerates",
    "finiteRegistryCarrier",
    "representedZeroArityOfArityZero",
    "finiteRepresentedAtomOfFiniteRegistry",
    "theorem zero_arity_carrier_exhaustiveness_from_repository_native_interface",
    "FRONTIER_OPEN / REPOSITORY_NATIVE_INTERFACE_REDUCTION_ONLY",
]

REQUIRED_DOC_TOKENS = [
    "Status: FRONTIER_OPEN / REPOSITORY_NATIVE_INTERFACE_REDUCTION_ONLY.",
    "This artifact replaces the local `CarrierData` dependency with an abstract repository-native interface target.",
    "This is a repository-native interface reduction only.",
    "This is not unrestricted Chronos-RR closure.",
    "This is not H4.1/FGL closure.",
    "This is not UniversalFiberEntropyGap closure.",
    "This is not P vs NP closure.",
    "This is not Clay-problem closure.",
    "`RepositoryNativeZeroArityInterface` instantiated by the active Chronos repository-native `Carrier` and `Registry`.",
]

FORBIDDEN_TOKENS = [
    "sorry",
    "axiom",
    "admit",
    "unrestricted Chronos-RR is closed",
    "H4.1/FGL is closed",
    "UniversalFiberEntropyGap is closed",
    "P vs NP is solved",
    "Clay problem is solved",
    "theorem-level closure achieved",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"verification failed: {message}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    for path in [LEAN_FILE, ARTIFACT, DOC]:
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    lean_text = LEAN_FILE.read_text()
    doc_text = DOC.read_text()
    artifact_text = ARTIFACT.read_text()
    artifact = json.loads(artifact_text)

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean_text, f"Lean token missing: {token}")

    for token in REQUIRED_DOC_TOKENS:
        require(token in doc_text, f"doc token missing: {token}")

    require("CarrierData" not in lean_text, "migration target must not use local CarrierData")

    combined = "\n".join([lean_text, doc_text, artifact_text])
    for token in FORBIDDEN_TOKENS:
        require(token not in combined, f"forbidden token present: {token}")

    require(
        artifact["status"] == "FRONTIER_OPEN / REPOSITORY_NATIVE_INTERFACE_REDUCTION_ONLY",
        "artifact status mismatch",
    )
    require(artifact["theorem_level_closure"] is False, "theorem closure must remain false")
    require(artifact["unrestricted_chronos_rr_closure"] is False, "Chronos-RR closure must remain false")
    require(artifact["h4_1_fgl_closure"] is False, "H4.1/FGL closure must remain false")
    require(artifact["universal_fiber_entropy_gap_closure"] is False, "UniversalFiberEntropyGap closure must remain false")
    require(artifact["p_vs_np_closure"] is False, "P vs NP closure must remain false")
    require(artifact["clay_problem_closure"] is False, "Clay closure must remain false")

    print("Repository-native zero-arity migration target verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
