import subprocess
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_temporal_relaxation_chain_status_snapshot_verifier():
    subprocess.run(
        ["python3", "tools/verify_temporal_relaxation_chain_status_snapshot.py"],
        cwd=ROOT,
        check=True,
    )

def test_temporal_relaxation_chain_status_snapshot_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/temporal_relaxation_chain_status_snapshot_2026_05_18.json").read_text()
    )
    assert data["status"] == "INTERFACE_CHAIN_CLOSED_FRONTIER_OPEN"
    assert data["audited_prs"] == [403, 404, 405, 406, 407, 408, 409]
    assert data["audit_verdict"] == "interface_closed_duplicate_compatible_alias_chain"
    assert "existence of UniformTemporalRelaxationWave" in data["genuine_non_interface_missing_lemmas"]
    assert "no unrestricted Chronos-RR" in data["boundary"]
    assert "no Clay problem" in data["boundary"]

def test_temporal_relaxation_chain_status_snapshot_boundary_doc():
    text = (ROOT / "docs/status/TEMPORAL_RELAXATION_CHAIN_STATUS_SNAPSHOT_2026_05_18.md").read_text()
    assert "Status: `INTERFACE_CHAIN_CLOSED_FRONTIER_OPEN`" in text
    assert "The chain is interface-closed." in text
    assert "Dashboard sync is an external next action." in text
    assert "No further progress possible without a new theorem-level input." in text
    assert "unrestricted Chronos-RR" in text
    assert "any Clay problem" in text
