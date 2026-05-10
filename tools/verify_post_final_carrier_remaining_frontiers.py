from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "Chronos/Frontier/PostFinalCarrierRemainingFrontiers.lean"
root = ROOT / "Chronos.lean"
doc = ROOT / "docs/status/CHRONOS_POST_FINAL_CARRIER_REMAINING_FRONTIERS_2026_05_10.md"
artifact = ROOT / "artifacts/chronos/post_final_carrier_remaining_frontiers_2026_05_10.json"

for path in [lean, root, doc, artifact]:
    assert path.exists(), f"missing required file: {path}"

lean_text = lean.read_text()
for token in [
    "PostFinalCarrierRemainingFrontier",
    "universalFiberEntropyGap",
    "depthBridgeBeyondSelectedFinalCarrierDomain",
    "chronosRRTheoremPromotion",
    "FinalCarrierExtractionSurfaceClosed",
    "UniversalFiberEntropyGapTheoremFrontierOpen",
    "DepthBridgeBeyondSelectedFinalCarrierDomainFrontierOpen",
    "ChronosRRTheoremPromotionFrontierOpen",
]:
    assert token in lean_text, token

assert "import Chronos.Frontier.PostFinalCarrierRemainingFrontiers" in root.read_text()

doc_text = doc.read_text()
for token in [
    "FINAL_CARRIER_EXTRACTION_SURFACE_CLOSED",
    "UniversalFiberEntropyGap theorem",
    "DepthBridge beyond selected final carrier domain",
    "Chronos-RR theorem promotion",
    "does not assert",
    "P vs NP closure",
    "Clay-problem closure",
]:
    assert token in doc_text, token

data = json.loads(artifact.read_text())
assert data["closed_surface"] == "FINAL_CARRIER_EXTRACTION_SURFACE_CLOSED"
assert data["boundary"]["universal_fiber_entropy_gap_closed"] is False
assert data["boundary"]["depth_bridge_beyond_selected_final_carrier_domain_closed"] is False
assert data["boundary"]["chronos_rr_theorem_closed"] is False
assert data["boundary"]["p_vs_np"] is False
assert data["boundary"]["clay_problem"] is False

for forbidden in [
    "solves P vs NP",
    "proves P vs NP",
    "resolves P vs NP",
    "solves the Clay",
    "resolves the Clay",
    "UniversalFiberEntropyGap theorem closed",
    "Chronos-RR theorem closed"
]:
    assert forbidden not in doc_text
    assert forbidden not in lean_text

print("Post-final-carrier remaining frontiers verified.")
