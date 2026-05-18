from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/AdmissibleRateThickToUniversalFiberEntropyGap.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/ADMISSIBLE_RATE_THICK_TO_UNIVERSAL_FIBER_ENTROPY_GAP_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/admissible_rate_thick_to_universal_fiber_entropy_gap_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.AdmissibleFiberMassUniformFloor",
    "structure UniversalFiberEntropyGapTarget",
    "def RateThickToUniversalFiberEntropyGapBridge",
    "theorem universalFiberEntropyGapTarget_from_rate_thick_target",
    "theorem RateThickToUniversalFiberEntropyGapBridge_solved",
    "def AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap",
    "theorem AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap_solved",
    "def AdmissibleUniversalFiberEntropyGapTarget",
    "theorem AdmissibleUniversalFiberEntropyGapTarget_solved",
    "def UnrestrictedUniversalFiberEntropyGapTarget",
    "theorem UnrestrictedUniversalFiberEntropyGapTarget_refuted",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.AdmissibleRateThickToUniversalFiberEntropyGap" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "ADMISSIBLE_UNIVERSAL_FIBER_ENTROPY_GAP_TARGET_CLOSED_RESTRICTED_ONLY",
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

print("Admissible rate-thick to universal fiber-entropy gap verified.")
