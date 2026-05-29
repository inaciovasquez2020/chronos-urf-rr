import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ytr_synthetic_injection_recovery_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_ytr_synthetic_injection_recovery_protocol.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "YTR_SYNTHETIC_INJECTION_RECOVERY_PROTOCOL_OK" in result.stdout

def test_ytr_synthetic_injection_recovery_artifact_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/ytr_synthetic_injection_recovery_protocol_2026_05_29.json").read_text()
    )
    assert artifact["status"] == "SYNTHETIC_PIPELINE_READINESS_ONLY_NOT_EMPIRICAL"
    assert artifact["classification"] == "synthetic pipeline-readiness infrastructure"
    for boundary in [
        "not empirical evidence",
        "not real likelihood evidence",
        "not independent replication",
        "not physical validation",
        "not new physics",
        "not new dark-matter science",
        "not Lambda-CDM failure evidence",
        "not dark matter replacement",
        "not predictive law closure",
        "not unrestricted Chronos-RR",
        "not unrestricted H4.1/FGL",
        "not P vs NP",
        "not any Clay problem",
    ]:
        assert boundary in artifact["boundary"]

def test_ytr_synthetic_injection_recovery_doc_boundary():
    text = (ROOT / "docs/status/YTR_SYNTHETIC_INJECTION_RECOVERY_PROTOCOL_2026_05_29.md").read_text()
    for token in [
        "Does not prove: empirical evidence.",
        "Does not prove: real likelihood evidence.",
        "Does not prove: independent replication.",
        "Does not prove: physical validation.",
        "Does not prove: new physics.",
        "Does not prove: new dark-matter science.",
        "Does not prove: Lambda-CDM failure evidence.",
        "Does not prove: dark matter replacement.",
        "Does not prove: predictive law closure.",
        "Does not prove: unrestricted Chronos-RR.",
        "Does not prove: unrestricted H4.1/FGL.",
        "Does not prove: P vs NP.",
        "Does not prove: any Clay problem.",
    ]:
        assert token in text
