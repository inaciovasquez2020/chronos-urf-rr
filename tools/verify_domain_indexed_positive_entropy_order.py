from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/DomainIndexedPositiveEntropyOrder.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/DOMAIN_INDEXED_POSITIVE_ENTROPY_ORDER_2026_05_17.md"
ARTIFACT = ROOT / "artifacts/chronos/domain_indexed_positive_entropy_order_2026_05_17.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "theorem no_common_uniform_bound",
    "theorem no_uniform_projection0",
    "theorem admissible0",
    "theorem DomainIndexedPositiveEntropyWitnessConstruction_order_solved",
    "def projectsToUniform0",
    "w.entropy_bound ≤ U.global_entropy",
    "exists_nat_gt",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.DomainIndexedPositiveEntropyOrder" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "THEOREM_SURFACE_CLOSED_ORDER_THEORETIC_ONLY",
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
    "proves P vs NP",
    "proves any Clay problem",
    "proves unrestricted Chronos-RR",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves H4.1/FGL",
]:
    require(forbidden not in doc, f"forbidden overclaim in doc: {forbidden}")
    require(forbidden not in json.dumps(artifact), f"forbidden overclaim in artifact: {forbidden}")

print("Domain-indexed positive entropy order surface verified.")
