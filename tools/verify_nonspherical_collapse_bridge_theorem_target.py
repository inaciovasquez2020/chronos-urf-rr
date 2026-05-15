from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/NonsphericalCollapseBridgeTheoremTarget.lean")
artifact = Path("artifacts/chronos/nonspherical_collapse_bridge_theorem_target_2026_05_15.json")
status = Path("docs/status/NONSPHERICAL_COLLAPSE_BRIDGE_THEOREM_TARGET_2026_05_15.md")
root = Path("Chronos.lean")

for path in [lean, artifact, status, root]:
    assert path.exists(), path

lean_text = lean.read_text()
artifact_text = artifact.read_text()
artifact_data = json.loads(artifact_text)
status_text = status.read_text()
root_text = root.read_text()

required_lean = [
    "import Chronos.Frontier.QuasiLocalCollapseGateConditionalBridge",
    "def NonsphericalCollapseBridgeTheoremTarget : Prop",
    "∀ I : QuasiLocalCollapseGateInput,",
    "QuasiLocalCollapseGateCondition I →",
    "MarginalOrTrappedNullExpansionSurface I",
    "theorem nonspherical_collapse_bridge_theorem_target_matches_missing_object",
    "NonsphericalCollapseBridgeTheoremTarget = NonsphericalCollapseBridgeLemma",
    "OPEN_PROBLEM_REQUIRED",
    "THEOREM_TARGET_ONLY_NOT_PROVED",
]

for phrase in required_lean:
    assert phrase in lean_text, phrase

for forbidden in ["axiom ", "admit", "sorry"]:
    assert forbidden not in lean_text, forbidden

assert artifact_data["status"] == "OPEN_PROBLEM_REQUIRED"
assert artifact_data["proof_status"] == "NOT_PROVED"
assert artifact_data["theorem_target"] == "NonsphericalCollapseBridgeTheoremTarget"
assert artifact_data["matches_existing_missing_object"] == "NonsphericalCollapseBridgeLemma"

required_status = [
    "Status: OPEN_PROBLEM_REQUIRED",
    "NonsphericalCollapseBridgeTheoremTarget",
    "NonsphericalCollapseBridgeTheoremTarget = NonsphericalCollapseBridgeLemma",
    "Theorem target only.",
    "No axiom, admit, or sorry is introduced.",
    "Does not prove:",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status_text, phrase

assert "import Chronos.Frontier.NonsphericalCollapseBridgeTheoremTarget" in root_text

combined = "\n".join([lean_text, artifact_text, status_text]).lower()

forbidden_overclaims = [
    "nonsphericalcollapsebridgetheoremtarget is proved",
    "proves nonsphericalcollapsebridgetheoremtarget",
    "proves an unconditional quasi-local collapse theorem",
    "proves unrestricted nonspherical collapse exclusion",
    "proves cosmic censorship",
    "proves the hoop conjecture",
    "proves unrestricted chronos-rr",
    "proves h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves any clay problem",
]

for token in forbidden_overclaims:
    assert token not in combined, token

print("Nonspherical collapse bridge theorem target verified.")
