from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/QuasiLocalCollapseGateConditionalBridge.lean")
artifact = Path("artifacts/chronos/quasi_local_collapse_gate_conditional_bridge_2026_05_15.json")
status = Path("docs/status/QUASI_LOCAL_COLLAPSE_GATE_CONDITIONAL_BRIDGE_2026_05_15.md")
root = Path("Chronos.lean")

for p in [lean, artifact, status, root]:
    assert p.exists(), p

lean_text = lean.read_text()
artifact_text = artifact.read_text()
artifact_data = json.loads(artifact_text)
status_text = status.read_text()
root_text = root.read_text()

required_lean = [
    "structure QuasiLocalCollapseGateInput",
    "def QuasiLocalCollapseGateCondition",
    "def MarginalOrTrappedNullExpansionSurface",
    "def NonsphericalCollapseBridgeLemma",
    "theorem quasi_local_collapse_gate_conditional_bridge",
    "CONDITIONAL_BRIDGE_ONLY",
    "NonsphericalCollapseBridgeLemma",
]

for phrase in required_lean:
    assert phrase in lean_text, phrase

assert artifact_data["status"] == "CONDITIONAL_BRIDGE_ONLY"
assert artifact_data["missing_object"] == "NonsphericalCollapseBridgeLemma"
assert "Chronos.Frontier.QuasiLocalCollapseGateConditionalBridge" in root_text

required_status = [
    "Status: CONDITIONAL_BRIDGE_ONLY",
    "Weakest missing object:",
    "NonsphericalCollapseBridgeLemma",
    "Conditional bridge only.",
    "Does not prove:",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status_text, phrase

combined = "\n".join([lean_text, artifact_text, status_text]).lower()

forbidden = [
    "proves an unconditional quasi-local collapse theorem",
    "proves unrestricted nonspherical collapse exclusion",
    "proves cosmic censorship",
    "proves the hoop conjecture",
    "proves unrestricted chronos-rr",
    "proves h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves any clay problem",
    "unconditional quasi-local collapse theorem is closed",
    "nonsphericalcollapsebridgelemma is proved",
]

for token in forbidden:
    assert token not in combined, token

print("Quasi-local collapse gate conditional bridge verified.")
