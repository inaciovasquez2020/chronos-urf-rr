#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/ytr_gravity_elastic_heldout_evidence_certificate_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_GRAVITY_ELASTIC_HELDOUT_EVIDENCE_CERTIFICATE_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/YtRGravityElasticHeldoutEvidenceCertificate.lean"

art_text = ART.read_text()
doc_text = DOC.read_text()
lean_text = LEAN.read_text()
data = json.loads(art_text)

assert data["object"] == "YtRGravityElasticHeldoutEvidenceCertificate"
assert data["status"] == "HELDOUT_EVIDENCE_CERTIFICATE_INTERFACE_ONLY_NO_EMPIRICAL_EVIDENCE_SUPPLIED"
assert "YtRGravityElasticBaselineComparisonRun" in art_text
assert "YtRGravityElasticBaselineComparisonRun" in lean_text

for token in [
    "holdoutSplitFrozen",
    "heldoutEvaluationExecuted",
    "uncertaintyAccountingExecuted",
    "acceptanceCriterionDeclared",
    "replicationPacketRecorded",
    "evidenceBoundaryPreserved",
]:
    assert token in art_text
    assert token in lean_text

for token in [
    "Does not prove:",
    "real data evidence supplied",
    "independent replication result",
    "any Clay problem",
]:
    assert token in doc_text

print("YTR_GRAVITY_ELASTIC_HELDOUT_EVIDENCE_CERTIFICATE_OK")
