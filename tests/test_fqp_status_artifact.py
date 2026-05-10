from pathlib import Path
import json

DOC = Path("docs/status/CHRONOS_FQP_STATUS_ARTIFACT_2026_05_10.md")
ARTIFACT = Path("artifacts/chronos/fqp_status_artifact_2026_05_10.json")


def test_fqp_status_artifact_only():
    doc = DOC.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    assert "STATUS_ARTIFACT_ONLY" in doc
    assert artifact["status"] == "STATUS_ARTIFACT_ONLY"


def test_fqp_boundaries():
    doc = DOC.read_text()

    required = [
        "FQP is not a frontier lemma.",
        "FQP is not a bridge interface.",
        "FQP is not a verifier target.",
        "FQP is not archived or discarded.",
        "FQP has no theorem role.",
        "FQP has no dependency link.",
        "FQP has no closure claim.",
    ]

    for token in required:
        assert token in doc


def test_fqp_forbidden_overclaims_absent():
    combined = DOC.read_text() + json.dumps(json.loads(ARTIFACT.read_text()))

    forbidden = [
        "FQP proves",
        "FQP closes",
        "FQP implies Chronos-RR",
        "FQP implies H4.1",
        "FQP implies FGL",
        "FQP implies P vs NP",
        "FQP solves",
    ]

    for token in forbidden:
        assert token not in combined
