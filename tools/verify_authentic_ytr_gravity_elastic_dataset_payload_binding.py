#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/authentic_ytr_gravity_elastic_dataset_payload_binding_2026_05_29.json"
DOC = ROOT / "docs/status/AUTHENTIC_YTR_GRAVITY_ELASTIC_DATASET_PAYLOAD_BINDING_2026_05_29.md"
LEAN = ROOT / "lean/Chronos/Frontier/AuthenticYtRGravityElasticDatasetPayloadBinding.lean"

art_text = ART.read_text()
doc_text = DOC.read_text()
lean_text = LEAN.read_text()
data = json.loads(art_text)

assert data["object"] == "AuthenticYtRGravityElasticDatasetPayloadBinding"
assert data["status"] == "CERTIFICATE_INTERFACE_ONLY_NO_AUTHENTIC_PAYLOAD_SUPPLIED"

for token in [
    "publicDataset",
    "payloadDigestVerified",
    "sourceIdentifierRecorded",
    "immutablePayloadPathRecorded",
    "licenseOrAccessTermsRecorded",
]:
    assert token in art_text
    assert token in lean_text

for token in [
    "Does not prove:",
    "unrestricted Chronos-RR",
    "P vs NP",
    "any Clay problem",
]:
    assert token in doc_text

print("AUTHENTIC_YTR_GRAVITY_ELASTIC_DATASET_PAYLOAD_BINDING_OK")
