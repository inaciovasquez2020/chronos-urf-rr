#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/YtROnslaughtBlindValidationProtocol.lean"
ART = ROOT / "artifacts/chronos/ytr_onslaught_blind_validation_protocol_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_ONSLAUGHT_BLIND_VALIDATION_PROTOCOL_2026_05_29.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

required_lean = [
    "YtRName",
    "YtRExpansion",
    "OnslaughtName",
    "YtROnslaughtBlindValidationProtocol",
    "readyForBlindLikelihood",
    "readyForNewPhysicsPromotion",
    "ytr_not_new_physics_before_blind_likelihood",
    "ytr_not_new_physics_before_independent_replication",
    "ytr_new_physics_promotion_requires_both_gates",
    "YTR_BLIND_VALIDATION_CANDIDATE_NOT_NEW_PHYSICS",
]

required_doc = [
    "Status: `YTR_BLIND_VALIDATION_CANDIDATE_NOT_NEW_PHYSICS`",
    "Does not prove: new physics.",
    "Does not prove: new dark-matter science.",
    "Does not prove: Lambda-CDM failure evidence.",
    "Does not prove: physical validation.",
    "Does not prove: predictive law closure.",
    "Does not prove: dark matter replacement.",
    "Does not prove: unrestricted Chronos-RR.",
    "Does not prove: unrestricted H4.1/FGL.",
    "Does not prove: P vs NP.",
    "Does not prove: any Clay problem.",
]

for path in [LEAN, ART, DOC, ROOT_IMPORT]:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")

lean_text = LEAN.read_text()
for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

doc_text = DOC.read_text()
for token in required_doc:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.YtROnslaughtBlindValidationProtocol" not in ROOT_IMPORT.read_text():
    raise SystemExit("missing Chronos root import")

artifact = json.loads(ART.read_text())
if artifact["status"] != "YTR_BLIND_VALIDATION_CANDIDATE_NOT_NEW_PHYSICS":
    raise SystemExit("wrong artifact status")

for forbidden in [
    "new physics",
    "new dark-matter science",
    "Lambda-CDM failure evidence",
    "physical validation",
    "predictive law closure",
    "dark matter replacement claim",
]:
    if forbidden not in artifact["forbidden_promotions"]:
        raise SystemExit(f"missing forbidden promotion: {forbidden}")

required_gates = artifact["promotion_rule"]["new_physics_admissible_only_if"]
if required_gates != [
    "blind likelihood improvement passes",
    "independent replication passes",
]:
    raise SystemExit("wrong promotion rule")

print("YTR_ONSLAUGHT_BLIND_VALIDATION_PROTOCOL_OK")
