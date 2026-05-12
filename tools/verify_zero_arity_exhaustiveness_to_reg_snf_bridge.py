#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos/Frontier/ZeroArityExhaustivenessToRegSNFBridge.lean"
ARTIFACT = ROOT / "artifacts/chronos/zero_arity_exhaustiveness_to_reg_snf_bridge.json"
STATUS = ROOT / "docs/status/CHRONOS_ZERO_ARITY_EXHAUSTIVENESS_TO_REG_SNF_BRIDGE_2026_05_12.md"
ROOT_IMPORT = ROOT / "Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "ZeroArityExhaustivenessToRepresentedZeroArityRegSNFBridge",
    "zero_arity_exhaustiveness_bridge_implies_represented_zero_arity_reg_snf",
    "zero_arity_exhaustiveness_bridge_implies_unrestricted_reg_snf",
    "repository_native_zero_arity_interface_bridge_implies_unrestricted_reg_snf",
    "zeroArityCarrierExhaustiveness_closed",
    "represented_zero_arity_reg_snf_implies_unrestricted_reg_snf",
    "FRONTIER_OPEN / ZERO_ARITY_EXHAUSTIVENESS_TO_REPRESENTED_REG_SNF_BRIDGE_REQUIRED",
]

REQUIRED_STATUS_TOKENS = [
    "RepositoryNativeZeroArityInterface",
    "ZeroArityCarrierExhaustiveness",
    "ZeroArityExhaustivenessToRepresentedZeroArityRegSNFBridge",
    "conditional bridge only",
    "does not prove",
]

REQUIRED_NON_CLAIMS = [
    "no proof of represented zero-arity Reg-SNF",
    "no unconditional unrestricted Reg-SNF",
    "no UniversalFiberEntropyGap",
    "no DepthBridge extension beyond selected final carrier domain",
    "no Chronos-RR theorem-level closure",
    "no H4.1/FGL theorem-level closure",
    "no P vs NP",
    "no Clay-problem closure",
]

FORBIDDEN_TOKENS = [
    "UniversalFiberEntropyGap is proved",
    "unconditional unrestricted Reg-SNF is proved",
    "Chronos-RR theorem-level closure is proved",
    "H4.1/FGL theorem-level closure is proved",
    "P vs NP is proved",
    "Clay-problem closure is proved",
]


def fail(msg: str) -> None:
    print(f"verification failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text()


def main() -> None:
    lean = require_file(LEAN)
    status = require_file(STATUS)
    root_import = require_file(ROOT_IMPORT)

    if "import Chronos.Frontier.ZeroArityExhaustivenessToRegSNFBridge" not in root_import:
        fail("Chronos.lean missing bridge import")

    for token in REQUIRED_LEAN_TOKENS:
        if token not in lean:
            fail(f"Lean file missing token: {token}")

    for token in REQUIRED_STATUS_TOKENS:
        if token not in status:
            fail(f"status doc missing token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in lean or token in status:
            fail(f"forbidden overclaim token present: {token}")

    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")

    data = json.loads(ARTIFACT.read_text())
    expected_status = "FRONTIER_OPEN / ZERO_ARITY_EXHAUSTIVENESS_TO_REPRESENTED_REG_SNF_BRIDGE_REQUIRED"
    if data.get("status") != expected_status:
        fail("artifact status mismatch")

    if data.get("theorem_level_closure") is not False:
        fail("artifact must keep theorem_level_closure false")

    non_claims = set(data.get("non_claims", []))
    for claim in REQUIRED_NON_CLAIMS:
        if claim not in non_claims:
            fail(f"artifact missing non-claim: {claim}")

    print("Zero-arity exhaustiveness to Reg-SNF bridge verified.")


if __name__ == "__main__":
    main()
