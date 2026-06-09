#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/external_qk_dini_name_resolution_certificate_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/ExternalQKDiniNameResolutionCertificate.lean"
status_doc = ROOT / "docs/status/EXTERNAL_QK_DINI_NAME_RESOLUTION_CERTIFICATE_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "ExternalQKDiniNameResolutionCertificate"
assert data["status"] == "EXTERNAL_NAME_RESOLUTION_CERTIFICATE_ONLY"
assert data["repository_name"] == "QKDini"
assert data["exact_external_name_status"] == "EXACT_EXTERNAL_NAME_UNRESOLVED"
assert data["candidate_external_anchor"] == "q-generalized Dini function"
assert data["candidate_source_id"] == "DOI:10.1155/2022/8496249"
assert data["minimal_missing_object"] == "ExternallyDerivedScientificQKDiniSourceObjectPayloadValue"

required_lean_terms = [
    "structure ExternalQKDiniNameResolutionCertificateData",
    "def ExternalQKDiniNameResolutionCertificate",
    "theorem externalQKDiniNameResolutionCertificate_repository_name",
    "theorem externalQKDiniNameResolutionCertificate_exact_name_unresolved",
    "theorem externalQKDiniNameResolutionCertificate_candidate_anchor",
]
for term in required_lean_terms:
    assert term in lean_text

assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "NAME_RESOLUTION_ONLY",
    "EXACT_QKDINI_EXTERNAL_NAME_UNRESOLVED",
    "CANDIDATE_ANCHOR_ONLY_Q_GENERALIZED_DINI_FUNCTION",
    "NO_EXTERNAL_QK_DINI_PAYLOAD_VALUE",
    "NO_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "exact external name status" in status_text.lower()
assert "import Chronos.Frontier.ExternalQKDiniNameResolutionCertificate" in root_text

print("EXTERNAL_QK_DINI_NAME_RESOLUTION_CERTIFICATE_OK")
