#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/RepositoryNativeSemanticRegistryComputation.lean")
ART = Path("artifacts/chronos/repository_native_semantic_registry_computation_2026_05_27.json")
DOC = Path("docs/status/REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_2026_05_27.md")
ROOT = Path("lean/Chronos.lean")

for path in [LEAN, ART, DOC, ROOT]:
    assert path.exists(), f"missing required file: {path}"

src = LEAN.read_text()
artifact_text = ART.read_text()
doc_text = DOC.read_text()
root_text = ROOT.read_text()
data = json.loads(artifact_text)

required_src_tokens = [
    "RepositoryNativeSemanticRegistryEntry",
    "RepositoryNativeSemanticRegistry",
    "repositoryNativeFiniteRegisteredHyperbolicRegistry",
    "repositoryNativeSemanticRankRate",
    "repositoryNativeFiberEntropyGap",
    "repositoryNativeSemanticSlack",
    "repositoryNativeSemanticRegistryRankGapInequality",
    "repositoryNativeSemanticRegistry_rank_eq",
    "repositoryNativeSemanticRegistry_gap_eq",
    "repositoryNativeSemanticRegistry_slack_eq",
    "repositoryNativeSemanticRegistry_rank_plus_slack_le_gap",
    "repositoryNativeSemanticRegistry_rank_lt_gap",
    "repositoryNativeSemanticRegistry_computation_exists",
    "entries.filter",
]

required_artifact_tokens = [
    "REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_CLOSED_ONE_REGISTRY_ONLY",
    "repositoryNativeSemanticRegistryComputation",
    "generalize repository-native semantic computation from one finite registry to arbitrary concrete target registries",
]

required_doc_tokens = [
    "REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_CLOSED_ONE_REGISTRY_ONLY",
    "RepositoryNativeSemanticRegistryEntry",
    "Does not prove",
    "repository-native semantic computation for arbitrary concrete target registries",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "P vs NP",
    "any Clay problem",
]

for token in required_src_tokens:
    assert token in src, token

for token in required_artifact_tokens:
    assert token in artifact_text, token

for token in required_doc_tokens:
    assert token in doc_text, token

assert "import Chronos.Frontier.RepositoryNativeSemanticRegistryComputation" in root_text

assert data["status"] == "REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_CLOSED_ONE_REGISTRY_ONLY"
assert data["object"] == "repositoryNativeSemanticRegistryComputation"
assert data["semantic_rank_rate"] + data["semantic_slack"] <= data["fiber_entropy_gap"]
assert data["semantic_slack"] > 0

for forbidden in [
    "proves UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves P vs NP",
    "proves any Clay problem",
]:
    assert forbidden not in src
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("REPOSITORY_NATIVE_SEMANTIC_REGISTRY_COMPUTATION_OK")
print(json.dumps({
    "object": data["object"],
    "status": data["status"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
