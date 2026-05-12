#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

LEAN_FILE = ROOT / "Chronos/Frontier/RepositoryNativeZeroArityGuardedFields.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_zero_arity_guarded_fields_2026_05_11.json"
DOC = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_ZERO_ARITY_GUARDED_FIELDS_2026_05_11.md"
AUDIT_TOOL = ROOT / "tools/audit_repository_native_zero_arity_interface.py"
LATEST_AUDIT = ROOT / "artifacts/chronos/repository_native_zero_arity_interface_audit_latest.json"

REQUIRED_LEAN_TOKENS = [
    "import Chronos.Frontier.RepositoryNativeZeroArityCarrierMigrationTarget",
    "structure GuardedRepositoryNativeZeroArityFields",
    "registryGenerates : Registry → Carrier → Prop",
    "finiteRegistry : Registry → Prop",
    "representedZeroArityRegistryPair : Carrier → Prop",
    "isFiniteRepresentedAtom : Carrier → Prop",
    "carrierRegistryGenerates",
    "finiteRegistryCarrier",
    "representedZeroArityOfArityZero",
    "finiteRepresentedAtomOfFiniteRegistry",
    "def toRepositoryNativeZeroArityInterface",
    "theorem guarded_fields_imply_zero_arity_carrier_exhaustiveness",
    "FRONTIER_OPEN / GUARDED_INTERFACE_FIELDS_ONLY",
]

REQUIRED_DOC_TOKENS = [
    "Status: FRONTIER_OPEN / GUARDED_INTERFACE_FIELDS_ONLY.",
    "This is a guarded field-obligation layer only.",
    "This does not instantiate the active Chronos Carrier/Registry interface.",
    "This is not unrestricted Chronos-RR closure.",
    "This is not H4.1/FGL closure.",
    "This is not UniversalFiberEntropyGap closure.",
    "This is not P vs NP closure.",
    "This is not Clay-problem closure.",
    "An active-native instantiation of the guarded fields.",
]

REQUIRED_MISSING_FIELDS = [
        "isFiniteRepresentedAtom",
    "carrierRegistryGenerates",
    "finiteRegistryCarrier",
    "representedZeroArityOfArityZero",
    "finiteRepresentedAtomOfFiniteRegistry",
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
    for path in [LEAN_FILE, ARTIFACT, DOC, AUDIT_TOOL, LATEST_AUDIT]:
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    lean_text = LEAN_FILE.read_text()
    artifact_text = ARTIFACT.read_text()
    doc_text = DOC.read_text()
    audit_tool_text = AUDIT_TOOL.read_text()
    latest_audit = json.loads(LATEST_AUDIT.read_text())
    artifact = json.loads(artifact_text)

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean_text, f"Lean token missing: {token}")

    for token in REQUIRED_DOC_TOKENS:
        require(token in doc_text, f"doc token missing: {token}")

    require(
        '"Chronos/Frontier/RepositoryNativeZeroArityGuardedFields.lean"' in audit_tool_text,
        "audit tool must skip guarded obligation file",
    )

    require(artifact["status"] == "FRONTIER_OPEN / GUARDED_INTERFACE_FIELDS_ONLY", "artifact status mismatch")
    require(artifact["theorem_level_closure"] is False, "artifact theorem closure must remain false")
    require(artifact["active_native_instantiation"] is False, "active native instantiation must remain false")
    require(artifact["unrestricted_chronos_rr_closure"] is False, "Chronos-RR closure must remain false")
    require(artifact["h4_1_fgl_closure"] is False, "H4.1/FGL closure must remain false")
    require(artifact["universal_fiber_entropy_gap_closure"] is False, "UniversalFiberEntropyGap closure must remain false")
    require(artifact["p_vs_np_closure"] is False, "P vs NP closure must remain false")
    require(artifact["clay_problem_closure"] is False, "Clay closure must remain false")

    for field in REQUIRED_MISSING_FIELDS:
        require(field in artifact["guarded_missing_fields"], f"guarded field missing from artifact: {field}")
        require(field in latest_audit["missing_fields"], f"latest audit must still list field as active-native missing: {field}")

    combined = "\n".join([lean_text, artifact_text, doc_text])
    for token in FORBIDDEN_TOKENS:
        require(token not in combined, f"forbidden token present: {token}")

    print("Repository-native zero-arity guarded fields verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
