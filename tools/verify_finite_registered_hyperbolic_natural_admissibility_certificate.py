#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/FiniteRegisteredHyperbolicNaturalAdmissibilityCertificate.lean")
ROOT = Path("lean/Chronos.lean")
ART = Path("artifacts/chronos/finite_registered_hyperbolic_natural_admissibility_certificate_2026_05_27.json")
DOC = Path("docs/status/FINITE_REGISTERED_HYPERBOLIC_NATURAL_ADMISSIBILITY_CERTIFICATE_2026_05_27.md")

src = LEAN.read_text()
root = ROOT.read_text()
data = json.loads(ART.read_text())
doc = DOC.read_text()

required_src_tokens = [
    "FiniteRegisteredHyperbolicRateThickAssembly",
    "finiteRegisteredHyperbolicConcreteRegistry",
    "FiniteRegisteredHyperbolicRateThickUniversalGapAssembly",
    "finiteRegisteredHyperbolicComputableTargetApplication",
    "finiteRegisteredHyperbolicNaturalAdmissibilityCertificate",
    "NaturalAdmissibilityDominanceCertificate",
    "finiteRegisteredHyperbolicTargetYieldsNaturalDominance",
    "Nonempty NaturalDominanceAdmissibleComputableClass",
]

for token in required_src_tokens:
    assert token in src, token

assert "import Chronos.Frontier.FiniteRegisteredHyperbolicNaturalAdmissibilityCertificate" in root
assert data["status"] == "FINITE_REGISTERED_HYPERBOLIC_CERTIFICATE_CLOSED_ONE_STACK_TARGET_ONLY"
assert data["object"] == "finiteRegisteredHyperbolicNaturalAdmissibilityCertificate"
assert data["next_missing_ingredient"] == (
    "construct NaturalAdmissibilityDominanceCertificate X for a genuinely application-derived non-toy target without hand-set rank and gap numerals"
)

required_boundaries = [
    "certificate construction for every concrete target application",
    "certificate construction for arbitrary finite registered hyperbolic registries",
    "raw opaque admissibility implies dominance",
    "RawToStructuredAdmissibilityDominance for the old raw class",
    "stability under admissible limits",
    "finite-support approximation theorem",
    "unrestricted semantic-rank-to-fiber-entropy bridge",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for boundary in required_boundaries:
    assert boundary in data["does_not_prove"], boundary
    assert boundary in doc, boundary

assert "FINITE_REGISTERED_HYPERBOLIC_CERTIFICATE_CLOSED_ONE_STACK_TARGET_ONLY" in doc
assert "finiteRegisteredHyperbolicNaturalAdmissibilityCertificate" in doc

print("FINITE_REGISTERED_HYPERBOLIC_NATURAL_ADMISSIBILITY_CERTIFICATE_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
