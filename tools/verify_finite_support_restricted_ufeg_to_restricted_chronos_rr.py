#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportRestrictedUFEGToRestrictedChronosRR.lean"
ARTIFACT = ROOT / "artifacts/chronos/finite_support_restricted_ufeg_to_restricted_chronos_rr_2026_05_18.json"
STATUS = ROOT / "docs/status/FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_CHRONOS_RR_2026_05_18.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

lean = LEAN.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()
root_import = ROOT_IMPORT.read_text()

required_lean = [
    "def RestrictedChronosRRFromFiniteSupport",
    "RestrictedUniversalFiberEntropyGapFromFiniteSupport D",
    "theorem restricted_chronos_rr_from_restricted_universal_fiber_entropy_gap_finite_support",
    "theorem finite_support_restricted_chronos_rr",
    "restricted_universal_fiber_entropy_gap_from_finite_support D",
    "theorem finite_support_restricted_chronos_rr_preserves_unconditional_ufeg_obstruction",
    "unconditional_universal_fiber_entropy_gap_obstructed",
]

for token in required_lean:
    assert token in lean, f"missing Lean token: {token}"

for forbidden in [
    "axiom",
    "admit",
    "sorry",
    "theorem unrestricted_universal_fiber_entropy_gap",
    "theorem unrestricted_chronos_rr",
    "theorem unrestricted_h41_fgl",
    "theorem p_vs_np",
    "theorem clay",
]:
    assert forbidden not in lean, f"forbidden Lean token present: {forbidden}"

assert artifact["status"] == "FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_CHRONOS_RR_CLOSED"

for phrase in [
    "finite positive support only",
    "restricted Chronos-RR surface only",
    "unconditional UniversalFiberEntropyGap obstruction remains valid",
    "does not prove unrestricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove H4.1/FGL unrestricted",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"], f"missing artifact boundary: {phrase}"

for phrase in [
    "Status: `FINITE_SUPPORT_RESTRICTED_UFEG_TO_RESTRICTED_CHRONOS_RR_CLOSED`.",
    "finite-support restricted UniversalFiberEntropyGap surface",
    "finite-support restricted Chronos-RR surface",
    "The unconditional arbitrary-fiber-mass obstruction remains valid.",
]:
    assert phrase in status, f"missing status phrase: {phrase}"

assert (
    "import Chronos.Frontier.FiniteSupportRestrictedUFEGToRestrictedChronosRR"
    in root_import
), "root Chronos.lean import missing"

print("Finite-support restricted UFEG to restricted Chronos-RR verified.")
