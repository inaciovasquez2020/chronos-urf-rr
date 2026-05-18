#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap.lean"
DOC = ROOT / "docs/status/RESTRICTED_RATE_THICK_COERCIVITY_TO_RESTRICTED_UNIVERSAL_FIBER_ENTROPY_GAP_2026_05_18.md"
ART = ROOT / "artifacts/chronos/restricted_rate_thick_coercivity_to_restricted_universal_fiber_entropy_gap_2026_05_18.json"
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
    "import Chronos.Frontier.MeasureFiberMassPackage",
    "structure RestrictedUniversalFiberEntropyGap",
    "def RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap",
    "theorem restricted_rate_thick_coercivity_to_restricted_gap_closed",
    "theorem restricted_gap_preserves_epsilon",
    "theorem restricted_gap_preserves_admissible_data",
    "theorem restricted_gap_preserves_uniform_floor",
    "inductive RestrictedUniversalFiberEntropyGapStatus",
    "unrestricted_gap_frontier_open",
    "theorem unrestricted_universal_fiber_entropy_gap_frontier_open",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in [
    "admit",
    "sorry",
    "axiom",
    "def UniversalFiberEntropyGap",
    "structure UniversalFiberEntropyGap",
    "theorem universal_fiber_entropy_gap",
    "theorem unrestricted_rate_thick_fiber_coercivity",
]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap" not in root_import:
    raise SystemExit("missing Chronos.lean import")

expected_status = "RESTRICTED_RATE_THICK_COERCIVITY_TO_RESTRICTED_GAP_CLOSED"
if artifact.get("status") != expected_status:
    raise SystemExit("incorrect artifact status")

required_boundaries = [
    "restricted-domain bridge only",
    "finite-support measure package only",
    "unrestricted UniversalFiberEntropyGap remains FRONTIER_OPEN",
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

print("Restricted rate-thick coercivity to restricted gap verified.")
