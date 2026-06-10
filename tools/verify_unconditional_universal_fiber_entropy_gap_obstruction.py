#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/UnconditionalUniversalFiberEntropyGapObstruction.lean"
ARTIFACT = ROOT / "artifacts/chronos/unconditional_universal_fiber_entropy_gap_obstruction_2026_05_18.json"
STATUS = ROOT / "docs/status/UNCONDITIONAL_UNIVERSAL_FIBER_ENTROPY_GAP_OBSTRUCTION_2026_05_18.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

lean = LEAN.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()
root_import = ROOT_IMPORT.read_text()

required = [
    "structure ArbitraryFiberMassData",
    "def UnconditionalFiberMassUniformFloor",
    "def unconditionalZeroFiberMassData",
    "theorem unconditionalZeroFiberMassData_no_uniform_floor",
    "theorem no_uniform_floor_of_arbitrarily_small",
    "theorem unconditional_universal_fiber_entropy_gap_obstructed",
    "¬ UnconditionalFiberMassUniformFloor",
]

for token in required:
    assert token in lean, f"missing Lean token: {token}"

for forbidden in [
    "axiom",
    "admit",
    "sorry",
    "theorem unrestricted_chronos_rr",
    "theorem p_vs_np",
    "theorem clay",
    "unconditional UniversalFiberEntropyGap proved",
]:
    assert forbidden not in lean, f"forbidden Lean token present: {forbidden}"

assert artifact["status"] == "UNCONDITIONAL_UFEG_OBSTRUCTED"

for phrase in [
    "refutes unconditional UniversalFiberEntropyGap over arbitrary fiber-mass data",
    "does not refute restricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"], f"missing boundary phrase: {phrase}"

status_flat = " ".join(status.split())

for phrase in [
    "Status: `UNCONDITIONAL_UFEG_OBSTRUCTED`.",
    "Arbitrary fiber-mass data does not imply a uniform positive lower bound.",
    "requires an additional positivity/coercivity assumption or a restricted domain",
    "This proves only the obstruction.",
]:
    assert " ".join(phrase.split()) in status_flat, f"missing status phrase: {phrase}"

assert (
    "import Chronos.Frontier.UnconditionalUniversalFiberEntropyGapObstruction"
    in root_import
), "root Chronos.lean import missing"

print("Unconditional UniversalFiberEntropyGap obstruction verified.")
