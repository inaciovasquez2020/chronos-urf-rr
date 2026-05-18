from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/OrderSurfaceToRateThickFiberCoercivityBridge.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/ORDER_SURFACE_TO_RATE_THICK_FIBER_COERCIVITY_BRIDGE_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/order_surface_to_rate_thick_fiber_coercivity_bridge_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.DomainIndexedPositiveEntropyOrder",
    "def OrderSurfaceAvailable",
    "def FiberMassUniformFloor",
    "structure RateThickFiberCoercivityTarget",
    "def OrderSurfaceToRateThickFiberCoercivityBridge",
    "def WeakestMissingMeasureFiberMassLemma",
    "def UniversalWeakestMissingMeasureFiberMassLemma",
    "theorem order_surface_available_solved",
    "theorem exact_coercivity_target_from_measure_fiber_mass_floor",
    "theorem OrderSurfaceToRateThickFiberCoercivityBridge_solved",
    "theorem unrestricted_rate_thick_reduced_to_measure_fiber_mass_floor",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.OrderSurfaceToRateThickFiberCoercivityBridge" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "CONDITIONAL_BRIDGE_CLOSED_MEASURE_FIBER_MASS_FRONTIER_OPEN",
    "unexpected artifact status",
)

require(
    artifact["weakest_missing_lemma"] == "UniversalWeakestMissingMeasureFiberMassLemma",
    "weakest missing lemma not recorded",
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

print("Order-surface to rate-thick fiber coercivity bridge verified.")
