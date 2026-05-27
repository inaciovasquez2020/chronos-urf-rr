#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/NamedConcreteNaturalAdmissibilityCertificate.lean")
ROOT = Path("lean/Chronos.lean")
ART = Path("artifacts/chronos/named_concrete_natural_admissibility_certificate_2026_05_27.json")
DOC = Path("docs/status/NAMED_CONCRETE_NATURAL_ADMISSIBILITY_CERTIFICATE_2026_05_27.md")

src = LEAN.read_text()
root = ROOT.read_text()
data = json.loads(ART.read_text())
doc = DOC.read_text()

required_src_tokens = [
    "firstNamedConcreteTargetApplication",
    "firstNamedConcreteNaturalAdmissibilityCertificate",
    "NaturalAdmissibilityDominanceCertificate",
    "firstNamedConcreteCertificateFrontier",
    "FirstTargetNaturalAdmissibilityCertificateFrontier",
    "firstNamedConcreteTargetYieldsNaturalDominance",
    "Nonempty NaturalDominanceAdmissibleComputableClass",
    "semanticRankRate := 0",
    "fiberEntropyGap := 1",
]

for token in required_src_tokens:
    assert token in src, token

assert "import Chronos.Frontier.NamedConcreteNaturalAdmissibilityCertificate" in root
assert data["status"] == "NAMED_CONCRETE_CERTIFICATE_CLOSED_ONE_TARGET_ONLY"
assert data["object"] == "firstNamedConcreteNaturalAdmissibilityCertificate"
assert data["next_missing_ingredient"] == (
    "construct NaturalAdmissibilityDominanceCertificate X for a non-toy target application already used by the Chronos-RR bridge stack"
)

required_boundaries = [
    "certificate construction for every concrete target application",
    "certificate construction for any non-toy target application",
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

assert "NAMED_CONCRETE_CERTIFICATE_CLOSED_ONE_TARGET_ONLY" in doc
assert "firstNamedConcreteNaturalAdmissibilityCertificate" in doc

print("NAMED_CONCRETE_NATURAL_ADMISSIBILITY_CERTIFICATE_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
