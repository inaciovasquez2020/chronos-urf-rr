from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/TemporalRelaxationChainStatusSnapshot.lean"
doc = ROOT / "docs/status/TEMPORAL_RELAXATION_CHAIN_STATUS_SNAPSHOT_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/temporal_relaxation_chain_status_snapshot_2026_05_18.json"

for path in [lean, doc, artifact]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

for token in [
    "inductive TemporalRelaxationChainSurfaceStatus",
    "def temporalRelaxationChainInterfaceStatus",
    "def temporalRelaxationChainTheoremBoundary",
    "theorem temporalRelaxationChain_interface_closed",
    "theorem temporalRelaxationChain_theorem_boundary_open",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

for token in [
    "Status: `INTERFACE_CHAIN_CLOSED_FRONTIER_OPEN`",
    "PR #403",
    "PR #404",
    "PR #405",
    "PR #406",
    "PR #407",
    "PR #408",
    "PR #409",
    "The chain is interface-closed.",
    "duplicate-compatible aliases or repackagings",
    "Dashboard sync is an external next action.",
    "No further progress possible without a new theorem-level input.",
    "existence of `UniformTemporalRelaxationWave`",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

if data.get("status") != "INTERFACE_CHAIN_CLOSED_FRONTIER_OPEN":
    raise SystemExit("wrong artifact status")

if data.get("audited_prs") != [403, 404, 405, 406, 407, 408, 409]:
    raise SystemExit("wrong audited PR list")

if data.get("audit_verdict") != "interface_closed_duplicate_compatible_alias_chain":
    raise SystemExit("wrong audit verdict")

print("Temporal relaxation chain status snapshot verified.")
