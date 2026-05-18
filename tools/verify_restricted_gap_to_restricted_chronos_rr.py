#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RestrictedUniversalFiberEntropyGapToRestrictedChronosRR.lean"
DOC = ROOT / "docs/status/RESTRICTED_UNIVERSAL_FIBER_ENTROPY_GAP_TO_RESTRICTED_CHRONOS_RR_2026_05_18.md"
ART = ROOT / "artifacts/chronos/restricted_universal_fiber_entropy_gap_to_restricted_chronos_rr_2026_05_18.json"
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
    "import Chronos.Frontier.RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap",
    "structure RestrictedChronosRRWitness",
    "def RestrictedUniversalFiberEntropyGapToRestrictedChronosRR",
    "theorem restricted_gap_to_restricted_chronos_rr_closed",
    "theorem restricted_chronos_rr_preserves_gap",
    "theorem restricted_chronos_rr_preserves_epsilon",
    "theorem restricted_chronos_rr_preserves_uniform_floor",
    "inductive RestrictedChronosRRStatus",
    "unrestricted_chronos_rr_frontier_open",
    "theorem unrestricted_chronos_rr_frontier_open",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in [
    "admit",
    "sorry",
    "axiom",
    "def ChronosRR",
    "structure ChronosRR",
    "theorem chronos_rr",
    "theorem unrestricted_chronos_rr ",
    "def H41FGL",
    "structure H41FGL",
]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.RestrictedUniversalFiberEntropyGapToRestrictedChronosRR" not in root_import:
    raise SystemExit("missing Chronos.lean import")

expected_status = "RESTRICTED_GAP_TO_RESTRICTED_CHRONOS_RR_CLOSED"
if artifact.get("status") != expected_status:
    raise SystemExit("incorrect artifact status")

required_boundaries = [
    "restricted Chronos-RR witness only",
    "restricted-domain bridge only",
    "finite-support measure package only",
    "unrestricted Chronos-RR remains FRONTIER_OPEN",
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
    "unrestricted Chronos-RR is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted RateThickFiberCoercivity is proved",
    "unrestricted FiberMassUniformFloor is proved",
    "H4.1/FGL is proved",
]:
    if forbidden in combined or forbidden in lean:
        raise SystemExit(f"forbidden overclaim present: {forbidden}")

print("Restricted gap to restricted Chronos-RR verified.")
