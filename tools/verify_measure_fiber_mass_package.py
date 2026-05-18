#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/MeasureFiberMassPackage.lean"
DOC = ROOT / "docs/status/MEASURE_FIBER_MASS_PACKAGE_2026_05_18.md"
ART = ROOT / "artifacts/chronos/measure_fiber_mass_package_2026_05_18.json"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

for path in [LEAN, DOC, ART, ROOT_IMPORT]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean = LEAN.read_text()
doc = DOC.read_text()
artifact_text = ART.read_text()
artifact = json.loads(artifact_text)
root_import = ROOT_IMPORT.read_text()

required_lean_tokens = [
    "structure MeasureFiberMassPackage extends FinitePositiveFiberMassAdmissiblePackage",
    "structure MeasureFiberMassUniformFloor",
    "fiber_mass_floor : ∀ n : ℕ, D.epsilon ≤ D.data.fiberMass n",
    "def finiteSupportPushforwardAdmissibleFiberMassData",
    "FinitePositiveFiberMassToAdmissibleFiberMassData",
    "theorem finite_support_pushforward_case_from_finite_positive",
    "theorem finite_support_pushforward_uniform_floor_from_finite_positive",
    "inductive MeasureFiberMassFrontierStatus",
    "unrestricted_measure_case_frontier_open",
    "theorem unrestricted_measure_fiber_mass_case_frontier_open",
    "structure RestrictedRateThickFiberCoercivity",
    "(D : MeasureFiberMassPackage) where",
    "def restricted_rate_thick_fiber_coercivity_from_finite_admissible_floor",
    "theorem restricted_rate_thick_fiber_coercivity_preserves_floor",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in [
    "fiber_mass_floor : D.fiber_mass_floor",
    "structure RestrictedRateThickFiberCoercivity\n    (D : MeasureFiberMassPackage) : Prop where",
    "admit",
    "sorry",
    "axiom",
    "unrestricted_rate_thick_fiber_coercivity_from_finite_admissible_floor",
    "unrestricted_universal_fiber_entropy_gap",
]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.MeasureFiberMassPackage" not in root_import:
    raise SystemExit("missing Chronos.lean import")

expected_status = "MEASURE_FIBER_MASS_PACKAGE_FINITE_SUPPORT_PUSHFORWARD_CLOSED_FRONTIER_OPEN"
if artifact.get("status") != expected_status:
    raise SystemExit("incorrect artifact status")

required_boundaries = [
    "finite-support pushforward case only",
    "restricted-domain RateThickFiberCoercivity bridge only",
    "unrestricted measure case remains FRONTIER_OPEN",
    "no unrestricted FiberMassUniformFloor",
    "no unrestricted RateThickFiberCoercivity",
    "no unrestricted UniversalFiberEntropyGap",
    "no unrestricted Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay-problem closure",
]

combined = "\n".join([doc, artifact_text])
for token in required_boundaries:
    if token not in combined:
        raise SystemExit(f"missing boundary token: {token}")

for forbidden in [
    "P vs NP is solved",
    "Clay problem is solved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted RateThickFiberCoercivity is proved",
    "unrestricted FiberMassUniformFloor is proved",
    "H4.1/FGL is proved",
]:
    if forbidden in combined or forbidden in lean:
        raise SystemExit(f"forbidden overclaim present: {forbidden}")

print("Measure fiber-mass package verified.")
