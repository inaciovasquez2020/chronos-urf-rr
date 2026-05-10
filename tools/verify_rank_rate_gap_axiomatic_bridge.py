from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "Chronos/Frontier/RankRateGapAxiomaticBridge.lean"
root = ROOT / "Chronos.lean"
doc = ROOT / "docs/status/CHRONOS_RANK_RATE_GAP_AXIOMATIC_BRIDGE_2026_05_10.md"
artifact = ROOT / "artifacts/chronos/rank_rate_gap_axiomatic_bridge_2026_05_10.json"

for path in [lean, root, doc, artifact]:
    assert path.exists(), f"missing required file: {path}"

lean_text = lean.read_text()
for token in [
    "import Chronos.Frontier.UniversalFiberEntropyGapNativeObligations",
    "axiom rank_rate_to_fiber_entropy_native",
    "CertifiedRankRateLowerBound ChronosNativeCarrierFamily n",
    "CertifiedFiberEntropyLowerBound ChronosNativeCarrierFamily n",
    "theorem ChronosNativeRankRateGapTheorem_axiomatic",
    "conditional_universal_fiber_entropy_gap_from_axiomatic_rank_rate_gap",
    "RankRateGapAxiomaticBridgeOnly",
]:
    assert token in lean_text, token

assert "import Chronos.Frontier.RankRateGapAxiomaticBridge" in root.read_text()

doc_text = doc.read_text()
for token in [
    "FRONTIER_OPEN_AXIOMATIC_BRIDGE_ONLY",
    "rank_rate_to_fiber_entropy_native",
    "ChronosNativeRankRateGapTheorem_axiomatic",
    "axiom-dependent bridge only",
    "theorem-level rank-rate proof",
    "unconditional universal fiber-entropy gap theorem closure",
    "DepthBridge beyond selected final carrier domain",
    "Chronos-RR theorem closure",
    "P vs NP closure",
    "Clay-problem closure",
]:
    assert token in doc_text, token

data = json.loads(artifact.read_text())
assert data["status"] == "FRONTIER_OPEN_AXIOMATIC_BRIDGE_ONLY"
assert data["axioms"] == ["rank_rate_to_fiber_entropy_native"]
assert data["boundary"]["rank_rate_gap_unconditional_proof"] is False
assert data["boundary"]["universal_fiber_entropy_gap_unconditional_closure"] is False
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
    "unconditional rank-rate closure",
    "unconditional universal fiber-entropy gap closure",
    "Chronos-RR theorem closed",
]:
    assert forbidden not in doc_text
    assert forbidden not in lean_text

print("RankRateGap axiomatic bridge verified.")
