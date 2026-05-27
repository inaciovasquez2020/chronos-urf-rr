#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/FirstTargetNaturalAdmissibilityCertificateFrontier.lean")
ROOT = Path("lean/Chronos.lean")
ART = Path("artifacts/chronos/first_target_natural_admissibility_certificate_frontier_2026_05_27.json")
DOC = Path("docs/status/FIRST_TARGET_NATURAL_ADMISSIBILITY_CERTIFICATE_FRONTIER_2026_05_27.md")

src = LEAN.read_text()
root = ROOT.read_text()
data = json.loads(ART.read_text())
doc = DOC.read_text()

required_src_tokens = [
    "FirstTargetNaturalAdmissibilityCertificateFrontier",
    "NaturalAdmissibilityDominanceCertificate X",
    "firstTargetNaturalAdmissibilityCertificateFrontier_to_natural",
    "Nonempty (NaturalDominanceAdmissibleComputableClass)",
    "base := X",
    "natural_certificate := h.certificate",
]

for token in required_src_tokens:
    assert token in src, token

assert "import Chronos.Frontier.FirstTargetNaturalAdmissibilityCertificateFrontier" in root
assert data["status"] == "FIRST_TARGET_CERTIFICATE_FRONTIER_ONLY"
assert data["object"] == "FirstTargetNaturalAdmissibilityCertificateFrontier"
assert data["next_missing_ingredient"] == (
    "construct NaturalAdmissibilityDominanceCertificate X for a named concrete target application"
)

required_boundaries = [
    "certificate construction for any concrete target application",
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

assert "FIRST_TARGET_CERTIFICATE_FRONTIER_ONLY" in doc
assert "NaturalAdmissibilityDominanceCertificate X" in doc

print("FIRST_TARGET_NATURAL_ADMISSIBILITY_CERTIFICATE_FRONTIER_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
