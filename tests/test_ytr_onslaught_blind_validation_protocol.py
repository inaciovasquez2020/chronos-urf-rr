import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_ytr_onslaught_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_ytr_onslaught_blind_validation_protocol.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "YTR_ONSLAUGHT_BLIND_VALIDATION_PROTOCOL_OK" in result.stdout

def test_ytr_artifact_blocks_new_physics_promotion_before_gates():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/ytr_onslaught_blind_validation_protocol_2026_05_29.json").read_text()
    )
    assert artifact["short_name"] == "YtR"
    assert artifact["expansion"] == "Yet-to-Replicate"
    assert artifact["status"] == "YTR_BLIND_VALIDATION_CANDIDATE_NOT_NEW_PHYSICS"
    assert artifact["promotion_rule"]["new_physics_admissible_only_if"] == [
        "blind likelihood improvement passes",
        "independent replication passes",
    ]

def test_ytr_doc_contains_no_overclaim_boundary():
    text = (ROOT / "docs/status/YTR_ONSLAUGHT_BLIND_VALIDATION_PROTOCOL_2026_05_29.md").read_text()
    for token in [
        "Does not prove: new physics.",
        "Does not prove: new dark-matter science.",
        "Does not prove: Lambda-CDM failure evidence.",
        "Does not prove: physical validation.",
        "Does not prove: predictive law closure.",
        "Does not prove: dark matter replacement.",
        "Does not prove: unrestricted Chronos-RR.",
        "Does not prove: unrestricted H4.1/FGL.",
        "Does not prove: P vs NP.",
        "Does not prove: any Clay problem.",
    ]:
        assert token in text
