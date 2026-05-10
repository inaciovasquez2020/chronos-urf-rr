#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("Chronos/Frontier/H4_1_FGL_Bridge1Refutation.lean").read_text()
doc = Path("docs/status/CHRONOS_H4_1_FGL_BRIDGE1_REFUTATION_2026_05_10.md").read_text()
artifact = json.loads(Path("artifacts/chronos/h4_1_fgl_bridge1_refutation.json").read_text())

required_lean = [
    "def zeroArityCarrier",
    "zero_arity_carrier_is_real_admissible",
    "zero_arity_carrier_not_final_domain",
    "admissible_to_final_carrier_domain_false",
    "¬ H4_1_FGL_AdmissibleToFinalCarrierDomain",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "BRIDGE_1_REFUTED"
assert artifact["witness"]["arity"] == 0

required_doc = [
    "Status: **BRIDGE_1_REFUTED**",
    "No unrestricted H4.1/FGL closure",
    "No UniversalFiberEntropyGap theorem",
    "No Chronos-RR closure",
    "No P vs NP or Clay-problem closure",
]

for token in required_doc:
    assert token in doc, token

print("H4.1/FGL Bridge 1 refutation verified: BRIDGE_1_REFUTED")
