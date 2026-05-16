#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/NonSymmetricCollapseCensorshipHoopFrontiers.lean"
doc = root / "docs/status/NONSYMMETRIC_COLLAPSE_CENSORSHIP_HOOP_FRONTIERS_2026_05_16.md"
artifact = root / "artifacts/chronos/nonsymmetric_collapse_censorship_hoop_frontiers_2026_05_16.json"
imports = root / "lean/Chronos.lean"

for path in [lean, doc, artifact, imports]:
    assert path.exists(), f"missing {path}"

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()
import_text = imports.read_text()
data = json.loads(artifact_text)

required_lean = [
    "structure NonSymmetricCollapseConfiguration",
    "def TrappedOrMarginallyTrappedSurface",
    "def NonSymmetricTrappedSurfaceCriterion",
    "structure CollapseEvolutionData",
    "structure CosmicCensorshipWitness",
    "def CosmicCensorshipTarget",
    "def CollapseToCensorshipBridge",
    "structure HoopConfiguration",
    "structure HoopConjectureWitness",
    "def HoopConjectureTarget",
    "def HoopFromQLGate",
    "structure NonSymmetricCollapseFrontierStatus",
    "def frontierStatus",
    "cosmicCensorshipPromotionBlocked",
    "hoopConjecturePromotionBlocked",
]

for token in required_lean:
    assert token in lean_text, token

required_doc = [
    "Status: FRONTIER_OPEN",
    "NonSymmetricTrappedSurfaceCriterion as FRONTIER_OPEN.",
    "CollapseToCensorshipBridge as FRONTIER_OPEN.",
    "HoopFromQLGate as FRONTIER_OPEN.",
    "FRONTIER_OPEN only.",
    "Does not prove:",
    "Cosmic Censorship",
    "the Hoop Conjecture",
]

for token in required_doc:
    assert token in doc_text, token

assert data["status"] == "FRONTIER_OPEN"
assert data["theorem_promotion"] is False
assert "NonSymmetricTrappedSurfaceCriterion" in data["frontier_open_targets"]
assert "CollapseToCensorshipBridge" in data["frontier_open_targets"]
assert "HoopFromQLGate" in data["frontier_open_targets"]
assert "import Chronos.Frontier.NonSymmetricCollapseCensorshipHoopFrontiers" in import_text

combined = "\n".join([lean_text, doc_text, artifact_text]).lower()

forbidden = [
    "proves nonsymmetrictrappedsurfacecriterion",
    "proves collapse tocensorshipbridge",
    "proves collapsetocensorshipbridge",
    "proves hoopfromqlgate",
    "proves cosmic censorship",
    "proves the hoop conjecture",
    "proves hoop conjecture",
    "proves unrestricted universalboundarycompactness",
    "proves unrestricted ql_collapsegate",
    "proves unrestricted chronos-rr",
    "proves h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves a clay problem",
    "cosmic censorship is closed",
    "hoop conjecture is closed",
    "unrestricted universalboundarycompactness is closed",
    "unrestricted ql_collapsegate is closed",
]

for token in forbidden:
    assert token not in combined, token

print("Non-symmetric collapse, censorship, and hoop frontiers verified.")
