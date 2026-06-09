#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/repository_local_qk_dini_source_object_payload_value_2026_06_09.json"
lean_file = ROOT / "lean/Chronos/Frontier/RepositoryLocalQKDiniSourceObjectPayloadValue.lean"
status_doc = ROOT / "docs/status/REPOSITORY_LOCAL_QK_DINI_SOURCE_OBJECT_PAYLOAD_VALUE_2026_06_09.md"
root_import = ROOT / "lean/Chronos.lean"

data = json.loads(artifact.read_text())
lean_text = lean_file.read_text()
status_text = status_doc.read_text()
root_text = root_import.read_text()

assert data["object"] == "RepositoryLocalQKDiniSourceObjectPayloadValue"
assert data["status"] == "REPOSITORY_LOCAL_PAYLOAD_VALUE_ONLY_NO_SCIENTIFIC_DERIVATION_CLAIM"
assert data["supersedes_unfilled_object"] == "ConcreteScientificQKDiniSourceObjectPayloadValue"
assert data["minimal_missing_object"] == "ExternallyDerivedScientificQKDiniSourceObjectPayloadValue"

required_lean_terms = [
    "structure RepositoryLocalQKDiniAdmissibility",
    "structure RepositoryLocalQKDiniSourceObjectPayload",
    "def RepositoryLocalQKDiniSourceObject",
    "def RepositoryLocalQKDiniSourceObjectPayloadValue",
    "def RepositoryLocalQKDiniSourceObjectPayloadValue.toCoefficientFamily",
    "def RepositoryLocalQKDiniSourceObjectPayloadValue.toUniformCoefficientBounds",
    "theorem repositoryLocalQKDiniSourceObjectPayloadValue_nonzero",
    "theorem repositoryLocalQKDiniSourceObjectPayloadValue_uniform_bound",
]
for term in required_lean_terms:
    assert term in lean_text

assert "scientific_derivation_claim : Prop" not in lean_text
assert "repository_local_admissibility" in lean_text
assert "axiom " not in lean_text
assert "sorry" not in lean_text

for boundary in [
    "RENAMED_REPOSITORY_LOCAL_NOT_SCIENTIFIC",
    "NO_SCIENTIFIC_DERIVATION_CLAIM_INSTANTIATED",
    "NO_EXTERNAL_QK_DINI_SOURCE_PAYLOAD",
    "NO_ANALYTIC_DINI_ESTIMATE_PROOF",
    "NO_FINAL_THEOREM_CLOSURE",
    "NO_FINAL_SCIENTIFIC_CLOSURE",
]:
    assert boundary in data["boundary"]

assert "renamed repository-local, not scientific" in status_text.lower()
assert "import Chronos.Frontier.RepositoryLocalQKDiniSourceObjectPayloadValue" in root_text

print("REPOSITORY_LOCAL_QK_DINI_SOURCE_OBJECT_PAYLOAD_VALUE_OK")
