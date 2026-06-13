#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_payload_field_proof_payloads_2026_06_13.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_PROOF_PAYLOADS_2026_06_13.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlPayloadFieldProofPayloads.lean"
root_lean = ROOT / "lean/Chronos.lean"

for path in [artifact, doc, lean, root_lean]:
    assert path.exists(), f"missing: {path}"

data = json.loads(artifact.read_text())
lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root_lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_PROOF_PAYLOADS"
assert data["status"] == "CONDITIONAL_PAYLOAD_FIELD_PROOF_PAYLOADS"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS"
assert data["lean_module"] == "Chronos.Frontier.RestrictedContinuationNormControlPayloadFieldProofPayloads"
assert data["stop_boundary"] == "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT"

for token in [
    "RestrictedContinuationNormControlPayloadFieldProofPayloadsHypotheses",
    "RestrictedContinuationNormControlPayloadFieldProofPayloadsAnalyticProofHypotheses",
    "RestrictedContinuationNormControlPayloadFieldProofPayloadsClosed",
    "theorem RestrictedContinuationNormControlPayloadFieldProofPayloads",
    "theorem RestrictedContinuationNormControlAnalyticEstimateFromPayloadFieldProofPayloads",
    "bridgeProofPayload",
    "derivativeIdentityProofPayload",
    "fluxNonnegativityProofPayload",
    "bootstrapBoundsProofPayload",
    "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT",
]:
    assert token in lean_text, f"missing Lean token: {token}"

for forbidden in ["sorry", "admit", "axiom", "opaque"]:
    assert forbidden not in lean_text, f"forbidden token in Lean: {forbidden}"

for token in [
    "CONDITIONAL_PAYLOAD_FIELD_PROOF_PAYLOADS",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS",
    "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT",
]:
    assert token in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.RestrictedContinuationNormControlPayloadFieldProofPayloads" in root_text

print("Restricted continuation norm-control payload field proof payloads verifier OK.")
print("Status: CONDITIONAL_PAYLOAD_FIELD_PROOF_PAYLOADS")
print("Stop boundary: STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT")
