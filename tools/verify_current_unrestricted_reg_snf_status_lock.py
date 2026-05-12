#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos/Frontier/CurrentUnrestrictedRegSNFStatusLock.lean"
ARTIFACT = ROOT / "artifacts/chronos/current_unrestricted_reg_snf_status_lock.json"
STATUS = ROOT / "docs/status/CHRONOS_CURRENT_UNRESTRICTED_REG_SNF_STATUS_LOCK_2026_05_12.md"
ROOT_IMPORT = ROOT / "Chronos.lean"

REQUIRED_LEAN_TOKENS = [
    "CurrentRepresentedZeroArityRegSNFClosed",
    "current_represented_zero_arity_reg_snf_closed",
    "represented_zero_arity_reg_snf_closed",
    "CurrentRealChronosAdmissibleUnrestrictedRegSNFClosed",
    "current_real_chronos_admissible_unrestricted_reg_snf_closed",
    "unrestricted_real_chronos_admissible_reg_snf_closed",
    "current_reg_snf_reaches_selected_depth_bridge_only",
    "current_reg_snf_no_global_chronos_rr_promotion",
    "CURRENT_REAL_CHRONOS_ADMISSIBLE_REG_SNF_CLOSED / SELECTED_DEPTHBRIDGE_ONLY",
]

REQUIRED_BOUNDARY = [
    "no UniversalFiberEntropyGap closure",
    "no DepthBridge extension beyond selected final carrier domain",
    "no Chronos-RR theorem-level closure",
    "no H4.1/FGL theorem-level closure",
    "no P vs NP closure",
    "no Clay-problem closure",
]

FORBIDDEN = [
    "UniversalFiberEntropyGap is proved",
    "DepthBridge extension beyond selected final carrier domain is proved",
    "Chronos-RR theorem-level closure is proved",
    "H4.1/FGL theorem-level closure is proved",
    "P vs NP is proved",
    "Clay-problem closure is proved",
]


def fail(msg: str) -> None:
    print(f"verification failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text()


def main() -> None:
    lean = read(LEAN)
    status = read(STATUS)
    root_import = read(ROOT_IMPORT)

    if "import Chronos.Frontier.CurrentUnrestrictedRegSNFStatusLock" not in root_import:
        fail("missing root import")

    for token in REQUIRED_LEAN_TOKENS:
        if token not in lean:
            fail(f"Lean token missing: {token}")

    for token in REQUIRED_BOUNDARY:
        if token not in lean or token not in status:
            fail(f"boundary token missing: {token}")

    for token in FORBIDDEN:
        if token in lean or token in status:
            fail(f"forbidden overclaim token present: {token}")

    data = json.loads(read(ARTIFACT))
    expected = "CURRENT_REAL_CHRONOS_ADMISSIBLE_REG_SNF_CLOSED / SELECTED_DEPTHBRIDGE_ONLY"

    if data.get("status") != expected:
        fail("artifact status mismatch")

    if data.get("theorem_level_closure") is not False:
        fail("theorem_level_closure must remain false")

    boundary = set(data.get("boundary", []))
    for token in REQUIRED_BOUNDARY:
        if token not in boundary:
            fail(f"artifact boundary missing: {token}")

    print("Current unrestricted Reg-SNF status lock verified.")


if __name__ == "__main__":
    main()
