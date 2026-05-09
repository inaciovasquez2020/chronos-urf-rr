import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_zero_arity_bifurcation_lock_artifact():
    data = json.loads((ROOT / "artifacts/chronos/zero_arity_bifurcation_lock.json").read_text())
    assert data["status"] == "BIFURCATION_LOCKED"
    assert data["accepted_paths"] == ["ZeroArityExclusion", "ZeroArityRepresentation"]
    assert data["weakest_sufficient_completion"] == "ZeroArityExclusion OR ZeroArityRepresentation"

def test_zero_arity_bifurcation_lock_boundaries():
    text = (ROOT / "docs/status/CHRONOS_ZERO_ARITY_BIFURCATION_LOCK_2026_05_09.md").read_text()
    for token in [
        "does not prove ZeroArityExclusion",
        "does not prove ZeroArityRepresentation",
        "does not resolve ZeroArityCarrierObstruction",
        "does not prove CarrierRegistryExhaustiveness",
        "does not prove Reg-SNF",
        "does not prove UniversalFiberEntropyGap",
        "does not prove DepthBridge",
        "does not close Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem",
    ]:
        assert token in text
