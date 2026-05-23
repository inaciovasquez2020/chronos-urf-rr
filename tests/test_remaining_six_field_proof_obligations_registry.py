import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_remaining_six_field_proof_obligations_registry_boundary():
    data = json.loads((ROOT / "artifacts/chronos/remaining_six_field_proof_obligations_registry_2026_05_23.json").read_text())
    assert data["status"] == "OPEN_PROOF_OBLIGATION_REGISTRY_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["obligation_count"] == 22
    assert len(data["obligations"]) == 22
    assert all(item["status"] == "OPEN" for item in data["obligations"])
    assert data["obligations"][0]["name"] == "AnalyticEstimateCandidatePacket"
    assert data["obligations"][-1]["name"] == "RestrictedGravityClosureBridgeProof"
    assert "proof of SixFieldAnalyticPackageHypothesis" in data["blocked_use"]
    assert "proof of any Clay problem" in data["blocked_use"]
    assert "unrestricted gravity closure" in data["still_not_proved"]
    assert data["next_admissible_object"] == "AnalyticEstimateCandidatePacket"
