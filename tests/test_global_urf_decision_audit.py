import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_global_urf_decision_audit_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_global_urf_decision_audit.py"],
        cwd=ROOT,
        check=True,
    )

def test_global_urf_decision_audit_claims_are_normalized():
    data = json.loads(
        (ROOT / "artifacts/chronos/global_urf_decision_audit_2026_05_18.json").read_text()
    )
    assert all(claim["form"] == "A_i => B_i" for claim in data["claims"])
    assert all(claim["A_i"] for claim in data["claims"])
    assert all(claim["B_i"] for claim in data["claims"])

def test_global_urf_decision_audit_has_sink_lemmas():
    data = json.loads(
        (ROOT / "artifacts/chronos/global_urf_decision_audit_2026_05_18.json").read_text()
    )
    sinks = data["dependency_dag_sinks"]
    assert "unrestricted uniform positivity/coercivity" in sinks
    assert "unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge" in sinks

def test_global_urf_decision_audit_preserves_boundaries():
    doc = (ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_2026_05_18.md").read_text()
    assert "Does not prove:" in doc
    assert "unrestricted UniversalFiberEntropyGap" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
