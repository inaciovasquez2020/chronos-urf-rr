#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/DerivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate.lean")
ART = Path("artifacts/chronos/derived_finite_registered_hyperbolic_natural_admissibility_certificate_2026_05_27.json")
DOC = Path("docs/status/DERIVED_FINITE_REGISTERED_HYPERBOLIC_NATURAL_ADMISSIBILITY_CERTIFICATE_2026_05_27.md")
ROOT = Path("lean/Chronos.lean")

for path in [LEAN, ART, DOC, ROOT]:
    assert path.exists(), f"missing required file: {path}"

src = LEAN.read_text()
artifact_text = ART.read_text()
doc_text = DOC.read_text()
root_text = ROOT.read_text()
data = json.loads(artifact_text)

required_src_tokens = [
    "derivedFiniteRegisteredHyperbolicObjectCount",
    "derivedFiniteRegisteredHyperbolicSemanticRankRate",
    "derivedFiniteRegisteredHyperbolicFiberEntropyGap",
    "derivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate",
    "NaturalDominanceAdmissibleComputableClass",
    "Nonempty",
]

required_artifact_tokens = [
    "DERIVED_FINITE_REGISTERED_HYPERBOLIC_CERTIFICATE_CLOSED_ONE_STACK_TARGET_ONLY",
    "derivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate",
    "next_missing_ingredient",
]

required_doc_tokens = [
    "DERIVED_FINITE_REGISTERED_HYPERBOLIC_CERTIFICATE_CLOSED_ONE_STACK_TARGET_ONLY",
    "Derived target data",
    "Does not prove",
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

assert "import Chronos.Frontier.DerivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate" in root_text

assert data["status"] == "DERIVED_FINITE_REGISTERED_HYPERBOLIC_CERTIFICATE_CLOSED_ONE_STACK_TARGET_ONLY"
assert data["object"] == "derivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate"

for forbidden in [
    "proves UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves P vs NP",
    "proves any Clay problem",
]:
    assert forbidden not in src
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("DERIVED_FINITE_REGISTERED_HYPERBOLIC_NATURAL_ADMISSIBILITY_CERTIFICATE_OK")
print(json.dumps({
    "object": data["object"],
    "status": data["status"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
