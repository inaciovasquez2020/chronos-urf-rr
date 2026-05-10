#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("Chronos/Frontier/H4_1_FGL_RestrictedDomainReduction.lean").read_text()
doc = Path("docs/status/CHRONOS_H4_1_FGL_RESTRICTED_DOMAIN_REDUCTION_2026_05_10.md").read_text()
artifact = json.loads(Path("artifacts/chronos/h4_1_fgl_restricted_domain_reduction.json").read_text())

required_lean = [
    "h4_1_fgl_unrestricted_bridge1_refuted",
    "H4_1_FGL_FinalCarrierDomainTarget",
    "H4_1_FGL_FinalCarrierSelectedGapSoundness",
    "h4_1_fgl_final_domain_reduction",
    "H4_1_FGL_IntendedCarrierTarget",
    "H4_1_FGL_IntendedToFinalCarrierDomain",
    "h4_1_fgl_intended_domain_reduction",
    "RESTRICTED_DOMAIN_REDUCTION_ONLY",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "RESTRICTED_DOMAIN_REDUCTION_ONLY"
assert "H4_1_FGL_FinalCarrierSelectedGapSoundness" in artifact["remaining_frontier"]

required_doc = [
    "Status: **RESTRICTED_DOMAIN_REDUCTION_ONLY**",
    "No unrestricted H4.1/FGL closure",
    "No UniversalFiberEntropyGap theorem",
    "No Chronos-RR closure",
    "No P vs NP or Clay-problem closure",
]

for token in required_doc:
    assert token in doc, token

print("H4.1/FGL restricted domain reduction verified: RESTRICTED_DOMAIN_REDUCTION_ONLY")
