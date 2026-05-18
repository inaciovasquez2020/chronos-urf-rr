from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/TerminalAdmissibleBoundaryChainCertificate.lean"
CHRONOS = ROOT / "lean/Chronos.lean"
DOC = ROOT / "docs/status/TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_2026_05_18.md"
ARTIFACT = ROOT / "artifacts/chronos/terminal_admissible_boundary_chain_certificate_2026_05_18.json"

def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(msg)

lean = LEAN.read_text()
chronos = CHRONOS.read_text()
doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.AdmissiblePNPBoundaryLockToClayBoundaryLock",
    "def TerminalAdmissibleBoundaryChainCertificate",
    "theorem terminalCertificate_from_clayBoundaryLockTarget",
    "theorem TerminalAdmissibleBoundaryChainCertificate_solved",
    "inductive TerminalBoundaryChainStatus",
    "| boundary_certificate_closed",
    "| theorem_promotion_blocked",
    "structure TerminalBoundaryChainAudit",
    "theorem TerminalBoundaryChainAudit_solved",
    "ClayStatus.frontier_open",
    "PNPStatus.frontier_open",
]

for token in required_lean_tokens:
    require(token in lean, f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    require(forbidden not in lean, f"forbidden Lean token present: {forbidden}")

require(
    "import Chronos.Frontier.TerminalAdmissibleBoundaryChainCertificate" in chronos,
    "missing Chronos.lean import",
)

require(
    artifact["status"] == "TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_CLOSED_NO_THEOREM_PROMOTION",
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
    "does not refute any Clay problem",
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
    "refutes any Clay problem",
]:
    require(forbidden not in doc, f"forbidden overclaim in doc: {forbidden}")
    require(forbidden not in json.dumps(artifact), f"forbidden overclaim in artifact: {forbidden}")

print("Terminal admissible boundary-chain certificate verified.")
