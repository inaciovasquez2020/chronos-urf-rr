#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "artifacts/chronos/repository_native_zero_arity_interface_audit_latest.json"
CLOSURE = ROOT / "Chronos/Frontier/RepositoryNativeZeroArityInterfaceClosure.lean"

REQUIRED_CLOSURE_TOKENS = [
    "carrierRegistryGenerates_of_registryGenerates",
    "finiteRegistryCarrier_of_finiteRegistry",
    "representedZeroArityOfArityZero_closed",
    "finiteRepresentedAtomOfFiniteRegistry_closed",
    "repositoryNativeZeroArityInterface_closed",
    "repositoryNativeZeroArityInterface_implies_zeroArityCarrierExhaustiveness",
    "zeroArityCarrierExhaustiveness_closed",
]

FORBIDDEN_OVERCLAIMS = [
    "unrestricted Reg-SNF is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR theorem-level closure",
    "H4.1/FGL theorem-level closure",
    "P vs NP is proved",
    "Clay-problem closure",
]

def fail(msg: str) -> None:
    print(f"verification failed: {msg}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not AUDIT.exists():
        fail(f"missing audit artifact: {AUDIT}")

    if not CLOSURE.exists():
        fail(f"missing closure file: {CLOSURE}")

    audit = json.loads(AUDIT.read_text())
    closure_text = CLOSURE.read_text()

    missing = set(audit.get("missing_fields", []))
    closed_fields = {
        "carrierRegistryGenerates",
        "finiteRegistryCarrier",
        "representedZeroArityOfArityZero",
        "finiteRepresentedAtomOfFiniteRegistry",
    }

    still_missing = sorted(closed_fields & missing)
    if still_missing:
        fail(f"closed guarded fields still listed missing: {still_missing}")

    for token in REQUIRED_CLOSURE_TOKENS:
        if token not in closure_text:
            fail(f"missing closure token: {token}")

    for token in FORBIDDEN_OVERCLAIMS:
        if token in closure_text:
            fail(f"forbidden overclaim token present: {token}")

    status = str(audit.get("status", ""))
    if "THEOREM_LEVEL" in status and "false" not in json.dumps(audit).lower():
        fail("audit status appears to promote theorem-level closure")

    print("Repository-native zero-arity guarded fields verified.")

if __name__ == "__main__":
    main()
