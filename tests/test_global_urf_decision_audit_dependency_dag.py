import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_global_urf_decision_audit_dependency_dag_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_global_urf_decision_audit_dependency_dag.py"],
        cwd=ROOT,
        check=True,
    )

def test_global_urf_decision_audit_dependency_dag_values():
    data = json.loads(
        (ROOT / "artifacts/chronos/global_urf_decision_audit_dependency_dag_2026_05_18.json").read_text()
    )
    assert data["status"] == "DAG_SURFACE_ONLY"
    assert data["edge_count"] == 16
    assert data["sink_node_count"] == 3
    assert "Sink:unrestricted uniform positivity/coercivity" in data["sink_nodes"]

def test_global_urf_decision_audit_dependency_dag_boundaries():
    doc = (ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_DEPENDENCY_DAG_2026_05_18.md").read_text()
    assert "Dependency DAG only." in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
