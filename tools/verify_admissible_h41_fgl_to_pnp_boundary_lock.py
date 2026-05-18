from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/AdmissibleH41FGLToPNPBoundaryLock.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/ADMISSIBLE_H41_FGL_TO_PNP_BOUNDARY_LOCK_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/admissible_h41_fgl_to_pnp_boundary_lock_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.AdmissibleChronosRRToH41FGL",
    "inductive PNPStatus",
    "| frontier_open",
    "structure PNPBoundaryLockTarget",
    "def H41FGLToPNPBoundaryLockBridge",
    "theorem pnpBoundaryLockTarget_from_h41FGLTarget",
    "theorem H41FGLToPNPBoundaryLockBridge_solved",
    "def AdmissibleH41FGLToPNPBoundaryLock",
    "theorem AdmissibleH41FGLToPNPBoundaryLock_solved",
    "def AdmissiblePNPBoundaryLockTarget",
    "theorem AdmissiblePNPBoundaryLockTarget_solved",
    "theorem pnp_boundary_status_frontier_open",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.AdmissibleH41FGLToPNPBoundaryLock" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "ADMISSIBLE_PNP_BOUNDARY_LOCK_CLOSED_NO_THEOREM_PROMOTION",
    "unexpected artifact status",
)

required_boundary = [
    "does not prove unrestricted RateThickFiberCoercivity",
    "does not prove unrestricted UniversalFiberEntropyGap",
    "does not prove unrestricted Chronos-RR",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
    "does not refute P vs NP",
    "does not prove any Clay problem",
]

for token in required_boundary:
    require(token in doc, f"missing doc boundary token: {token}")
    require(any(token in b for b in artifact["boundary"]), f"missing artifact boundary token: {token}")

for forbidden in [
    "proves unrestricted RateThickFiberCoercivity",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves unrestricted H4.1/FGL",
    "proves P vs NP",
    "refutes P vs NP",
    "proves any Clay problem",
]:
    require(forbidden not in doc, f"forbidden overclaim in doc: {forbidden}")
    require(forbidden not in json.dumps(artifact), f"forbidden overclaim in artifact: {forbidden}")

print("Admissible H4.1/FGL to P vs NP boundary lock verified.")
