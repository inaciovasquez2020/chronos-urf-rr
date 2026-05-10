from pathlib import Path
import json

DOC = Path("docs/status/CHRONOS_FQP_STATUS_ARTIFACT_2026_05_10.md")
ARTIFACT = Path("artifacts/chronos/fqp_status_artifact_2026_05_10.json")

doc = DOC.read_text()
artifact = json.loads(ARTIFACT.read_text())

required_doc_tokens = [
    "STATUS_ARTIFACT_ONLY",
    "FQP is a named toolkit input/layer.",
    "FQP is not a frontier lemma.",
    "FQP is not a bridge interface.",
    "FQP is not a verifier target.",
    "FQP is not archived or discarded.",
    "FQP has no theorem role.",
    "FQP has no dependency link.",
    "FQP has no closure claim.",
]

for token in required_doc_tokens:
    assert token in doc, token

assert artifact["name"] == "FQP"
assert artifact["status"] == "STATUS_ARTIFACT_ONLY"
assert "named_toolkit_input_layer" in artifact["established"]
assert "frontier_lemma" in artifact["not_established"]
assert "bridge_interface" in artifact["not_established"]
assert "verifier_target" in artifact["not_established"]
assert "closure_claim" in artifact["not_established"]
assert "no_closure_claim" in artifact["boundary"]

forbidden = [
    "FQP proves",
    "FQP closes",
    "FQP implies Chronos-RR",
    "FQP implies H4.1",
    "FQP implies FGL",
    "FQP implies P vs NP",
    "FQP solves",
]

combined = doc + json.dumps(artifact)

for token in forbidden:
    assert token not in combined, token

print("FQP status artifact verified: STATUS_ARTIFACT_ONLY")
