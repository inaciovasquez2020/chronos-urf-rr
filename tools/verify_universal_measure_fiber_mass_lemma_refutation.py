from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/UniversalWeakestMissingMeasureFiberMassLemmaRefutation.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/UNIVERSAL_MEASURE_FIBER_MASS_LEMMA_REFUTATION_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/universal_measure_fiber_mass_lemma_refutation_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.OrderSurfaceToRateThickFiberCoercivityBridge",
    "def zeroFiberMassData",
    "theorem zeroFiberMassData_no_uniform_floor",
    "theorem UniversalWeakestMissingMeasureFiberMassLemma_refuted",
    "theorem UnrestrictedRateThickFiberCoercivityTarget_refuted",
    "def RestrictedMeasureFiberMassFloorTarget",
    "theorem RestrictedMeasureFiberMassFloorTarget_solved",
    "not_lt_of_ge",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.UniversalWeakestMissingMeasureFiberMassLemmaRefutation" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "UNRESTRICTED_MEASURE_FIBER_MASS_LEMMA_REFUTED_RESTRICTED_TARGET_CLOSED",
    "unexpected artifact status",
)

require(
    "UniversalWeakestMissingMeasureFiberMassLemma" in artifact["refuted"],
    "missing universal lemma refutation record",
)

require(
    "UnrestrictedRateThickFiberCoercivityTarget" in artifact["refuted"],
    "missing unrestricted target refutation record",
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

print("Universal measure/fiber-mass lemma refutation verified.")
