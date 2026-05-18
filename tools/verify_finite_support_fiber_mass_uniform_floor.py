#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportFiberMassUniformFloor.lean"
ARTIFACT = ROOT / "artifacts/chronos/finite_support_fiber_mass_uniform_floor_2026_05_18.json"
STATUS = ROOT / "docs/status/FINITE_SUPPORT_FIBER_MASS_UNIFORM_FLOOR_2026_05_18.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

lean = LEAN.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()
root_import = ROOT_IMPORT.read_text()

required_lean = [
    "structure FiniteSupportPositiveFiberMass",
    "def FiniteSupportFiberMassUniformFloor",
    "theorem finite_support_fiber_mass_uniform_floor",
    "Finset.univ.image D.mass",
    "Finset.min'",
    "theorem restricted_rate_thick_fiber_coercivity_from_finite_support",
    "theorem restricted_universal_fiber_entropy_gap_from_finite_support",
]

for token in required_lean:
    assert token in lean, f"missing Lean token: {token}"

for forbidden in [
    "axiom",
    "admit",
    "sorry",
    "theorem unrestricted_universal_fiber_entropy_gap",
    "theorem unrestricted_chronos_rr",
    "theorem p_vs_np",
    "theorem clay",
]:
    assert forbidden not in lean, f"forbidden Lean token present: {forbidden}"

assert artifact["status"] == "FINITE_SUPPORT_FIBER_MASS_UNIFORM_FLOOR_CLOSED"

for phrase in [
    "finite positive support only",
    "restricted UniversalFiberEntropyGap surface only",
    "does not refute unconditional UniversalFiberEntropyGap obstruction",
    "does not prove unrestricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"], f"missing artifact boundary: {phrase}"

for phrase in [
    "Status: `FINITE_SUPPORT_FIBER_MASS_UNIFORM_FLOOR_CLOSED`.",
    "finite positive fiber-mass support supplies a uniform positive floor",
    "The unconditional arbitrary-fiber-mass obstruction remains valid.",
]:
    assert phrase in status, f"missing status phrase: {phrase}"

assert (
    "import Chronos.Frontier.FiniteSupportFiberMassUniformFloor"
    in root_import
), "root Chronos.lean import missing"

print("FiniteSupportFiberMassUniformFloor verified.")
