from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/AdmissibleUniversalFiberEntropyGapToChronosRR.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/ADMISSIBLE_UNIVERSAL_FIBER_ENTROPY_GAP_TO_CHRONOS_RR_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/admissible_universal_fiber_entropy_gap_to_chronos_rr_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.AdmissibleRateThickToUniversalFiberEntropyGap",
    "structure ChronosRRTarget",
    "def UniversalFiberEntropyGapToChronosRRBridge",
    "theorem chronosRRTarget_from_universalFiberEntropyGapTarget",
    "theorem UniversalFiberEntropyGapToChronosRRBridge_solved",
    "def AdmissibleUniversalFiberEntropyGapToChronosRR",
    "theorem AdmissibleUniversalFiberEntropyGapToChronosRR_solved",
    "def AdmissibleChronosRRTarget",
    "theorem AdmissibleChronosRRTarget_solved",
    "def UnrestrictedChronosRRTarget",
    "theorem UnrestrictedChronosRRTarget_refuted",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.AdmissibleUniversalFiberEntropyGapToChronosRR" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "ADMISSIBLE_CHRONOS_RR_TARGET_CLOSED_RESTRICTED_ONLY",
    "unexpected artifact status",
)

required_boundary = [
    "does not prove unrestricted RateThickFiberCoercivity",
    "does not prove unrestricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]

for token in required_boundary:
    require(token in doc, f"missing doc boundary token: {token}")
    require(any(token in b for b in artifact["boundary"]), f"missing artifact boundary token: {token}")

for forbidden in [
    "proves unrestricted RateThickFiberCoercivity",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "proves any Clay problem",
]:
    require(forbidden not in doc, f"forbidden overclaim in doc: {forbidden}")
    require(forbidden not in json.dumps(artifact), f"forbidden overclaim in artifact: {forbidden}")

print("Admissible universal fiber-entropy gap to Chronos-RR verified.")
