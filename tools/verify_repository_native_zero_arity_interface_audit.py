#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

LEAN_FILE = ROOT / "Chronos/Frontier/RepositoryNativeZeroArityInterfaceAudit.lean"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_zero_arity_interface_audit_2026_05_11.json"
LATEST = ROOT / "artifacts/chronos/repository_native_zero_arity_interface_audit_latest.json"
DOC = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_ZERO_ARITY_INTERFACE_AUDIT_2026_05_11.md"
AUDIT_TOOL = ROOT / "tools/audit_repository_native_zero_arity_interface.py"

REQUIRED_LEAN_TOKENS = [
    "import Chronos.Frontier.RepositoryNativeZeroArityCarrierMigrationTarget",
    "inductive RepositoryNativeZeroArityField",
    "| carrier",
    "| registry",
    "| arity",
    "| carrierRegistry",
    "| registryGenerates",
    "| finiteRegistry",
    "| representedZeroArityRegistryPair",
    "| isFiniteRepresentedAtom",
    "| carrierRegistryGenerates",
    "| finiteRegistryCarrier",
    "| representedZeroArityOfArityZero",
    "| finiteRepresentedAtomOfFiniteRegistry",
    "theorem required_field_count_eq",
    "FRONTIER_OPEN / ACTIVE_NATIVE_INTERFACE_AUDIT_ONLY",
]

REQUIRED_DOC_TOKENS = [
    "Status: FRONTIER_OPEN / ACTIVE_NATIVE_INTERFACE_AUDIT_ONLY.",
    "This is an audit only.",
    "This does not instantiate the active Chronos Carrier/Registry interface.",
    "This is not unrestricted Chronos-RR closure.",
    "This is not H4.1/FGL closure.",
    "This is not UniversalFiberEntropyGap closure.",
    "This is not P vs NP closure.",
    "This is not Clay-problem closure.",
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
    for path in [LEAN_FILE, ARTIFACT, LATEST, DOC, AUDIT_TOOL]:
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    lean_text = LEAN_FILE.read_text()
    artifact_text = ARTIFACT.read_text()
    latest_text = LATEST.read_text()
    doc_text = DOC.read_text()
    audit_text = AUDIT_TOOL.read_text()

    artifact = json.loads(artifact_text)
    latest = json.loads(latest_text)

    for token in REQUIRED_LEAN_TOKENS:
        require(token in lean_text, f"Lean token missing: {token}")

    for token in REQUIRED_DOC_TOKENS:
        require(token in doc_text, f"doc token missing: {token}")

    combined = "\n".join([lean_text, artifact_text, latest_text, doc_text, audit_text])
    for token in FORBIDDEN_TOKENS:
        require(token not in combined, f"forbidden token present: {token}")

    require(artifact["status"] == "FRONTIER_OPEN / ACTIVE_NATIVE_INTERFACE_AUDIT_ONLY", "artifact status mismatch")
    require(latest["status"] == "FRONTIER_OPEN / ACTIVE_NATIVE_INTERFACE_AUDIT_ONLY", "latest audit status mismatch")
    require(artifact["theorem_level_closure"] is False, "artifact theorem closure must remain false")
    require(latest["theorem_level_closure"] is False, "latest theorem closure must remain false")
    require(isinstance(latest["missing_fields"], list), "latest missing_fields must be a list")
    require(isinstance(latest["candidate_files"], dict), "latest candidate_files must be an object")

    print("Repository-native zero-arity interface audit verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
