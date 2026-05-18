from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/FinitePositiveFiberMassUniformFloor.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/FINITE_POSITIVE_FIBER_MASS_UNIFORM_FLOOR_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/finite_positive_fiber_mass_uniform_floor_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "structure FiniteFiberMassData",
    "def FiniteFiberMassUniformFloor",
    "theorem finite_positive_fiber_mass_uniform_floor",
    "Finset.univ.image M.mass",
    "Finset.min'_mem",
    "Finset.min'_le",
    "theorem FinitePositiveFiberMassUniformFloorTheorem_solved"
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.FinitePositiveFiberMassUniformFloor" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "FINITE_POSITIVE_FIBER_MASS_UNIFORM_FLOOR_CLOSED",
    "unexpected artifact status",
)

required_boundary = [
    "does not prove unrestricted FiberMassUniformFloor for arbitrary FiberMassData",
    "does not prove unrestricted RateThickFiberCoercivity",
    "does not prove unrestricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
    "does not refute P vs NP",
    "does not prove any Clay problem",
    "does not refute any Clay problem",
]

for token in required_boundary:
    require(token in doc, f"missing doc boundary token: {token}")
    require(any(token in b for b in artifact["boundary"]), f"missing artifact boundary token: {token}")

print("Finite positive fiber-mass uniform floor verified.")
