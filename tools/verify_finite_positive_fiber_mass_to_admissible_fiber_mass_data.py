#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/FinitePositiveFiberMassToAdmissibleFiberMassData.lean"
DOC = ROOT / "docs/status/FINITE_POSITIVE_FIBER_MASS_TO_ADMISSIBLE_FIBER_MASS_DATA_2026_05_18.md"
ART = ROOT / "artifacts/chronos/finite_positive_fiber_mass_to_admissible_fiber_mass_data_2026_05_18.json"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

for path in [LEAN, DOC, ART, ROOT_IMPORT]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean = LEAN.read_text()
doc = DOC.read_text()
root_import = ROOT_IMPORT.read_text()
artifact_text = ART.read_text()
artifact = json.loads(artifact_text)

required_lean_tokens = [
    "structure FinitePositiveFiberMassAdmissiblePackage extends AdmissibleFiberMassData",
    "def FinitePositiveFiberMassToAdmissibleFiberMassData",
    "D.toAdmissibleFiberMassData",
    "theorem finite_positive_fiber_mass_to_admissible_fiber_mass_data_closed",
    "theorem finite_positive_fiber_mass_to_admissible_fiber_mass_data_preserves_epsilon",
    "theorem finite_positive_fiber_mass_to_admissible_fiber_mass_data_preserves_floor",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in [
    "structure AdmissibleFiberMassData",
    "Classical.choice",
    "List.foldr",
    "finitePositiveFiberMassFloor",
    "admit",
    "sorry",
]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.FinitePositiveFiberMassToAdmissibleFiberMassData" not in root_import:
    raise SystemExit("missing Chronos.lean import")

if artifact.get("status") != "FINITE_POSITIVE_FIBER_MASS_TO_ADMISSIBLE_FIBER_MASS_DATA_CLOSED":
    raise SystemExit("incorrect artifact status")

required_boundaries = [
    "admissible payload projection only",
    "finite-positive package transfer only",
    "no new minimum-over-list theorem",
    "no redeclaration of AdmissibleFiberMassData",
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
    "unrestricted Chronos-RR is proved",
    "H4.1/FGL is proved",
]:
    if forbidden in combined or forbidden in lean:
        raise SystemExit(f"forbidden overclaim present: {forbidden}")

print("Finite positive fiber-mass to admissible fiber-mass data verified.")
