import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_analytic_estimate_candidate_packet_boundary():
    data = json.loads((ROOT / "artifacts/chronos/analytic_estimate_candidate_packet_2026_05_23.json").read_text())
    assert data["status"] == "CANDIDATE_PACKET_ONLY_NO_ANALYTIC_ESTIMATE_PROOF"
    assert data["candidate_count"] == 10
    assert len(data["candidates"]) == 10
    assert all(item["proof_supplied"] is False for item in data["candidates"])
    assert data["candidates"][0]["name"] == "SemiclassicalEinsteinKGFixedPointTemplate"
    assert data["candidates"][-1]["name"] == "ConcreteSixFieldSlotEstimateGap"
    assert "localExistenceSlot" in data["unfilled_slots_after_packet"]
    assert "collapseGateTriggerSlot" in data["unfilled_slots_after_packet"]
    assert "proof of SixFieldAnalyticPackageHypothesis" in data["blocked_use"]
    assert "proof of any Clay problem" in data["blocked_use"]
    assert data["next_admissible_object"] == "FilledConcreteInitialDataClass"
