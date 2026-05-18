from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/AdmissibleFiberMassUniformFloor.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/ADMISSIBLE_FIBER_MASS_UNIFORM_FLOOR_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/admissible_fiber_mass_uniform_floor_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.UniversalWeakestMissingMeasureFiberMassLemmaRefutation",
    "structure AdmissibleFiberMassData",
    "def AdmissibleFiberMassUniformFloor",
    "theorem AdmissibleFiberMassUniformFloor_solved",
    "def AdmissibleRateThickFiberCoercivityTarget",
    "theorem AdmissibleRateThickFiberCoercivityTarget_solved",
    "def constantOneAdmissibleFiberMassData",
    "theorem AdmissibleFiberMassData_nonempty",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.AdmissibleFiberMassUniformFloor" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "ADMISSIBLE_FIBER_MASS_FLOOR_CLOSED_RESTRICTED_ONLY",
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

print("Admissible fiber-mass uniform floor verified.")
