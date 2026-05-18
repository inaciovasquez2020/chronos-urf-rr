import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_global_urf_decision_audit_numeric_snapshot_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_global_urf_decision_audit_numeric_snapshot.py"],
        cwd=ROOT,
        check=True,
    )

def test_global_urf_decision_audit_numeric_snapshot_values():
    data = json.loads(
        (ROOT / "artifacts/chronos/global_urf_decision_audit_numeric_snapshot_2026_05_18.json").read_text()
    )
    assert data["claims_total"] == 4
    assert data["proved_surface_percent"] == 25.0
    assert data["conditional_surface_percent"] == 25.0
    assert data["open_or_countermodel_percent"] == 50.0
    assert data["latest_full_pytest_passed"] == 958

def test_global_urf_decision_audit_numeric_snapshot_boundaries():
    doc = (ROOT / "docs/status/GLOBAL_URF_DECISION_AUDIT_NUMERIC_SNAPSHOT_2026_05_18.md").read_text()
    assert "Numeric snapshot only." in doc
    assert "unrestricted `UniversalFiberEntropyGap`" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
