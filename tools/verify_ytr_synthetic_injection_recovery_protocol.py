#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/YtRSyntheticInjectionRecoveryProtocol.lean"
ART = ROOT / "artifacts/chronos/ytr_synthetic_injection_recovery_protocol_2026_05_29.json"
DOC = ROOT / "docs/status/YTR_SYNTHETIC_INJECTION_RECOVERY_PROTOCOL_2026_05_29.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, DOC, ROOT_IMPORT]:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")

lean_text = LEAN.read_text()
required_lean_tokens = [
    "YTR_SYNTHETIC_INJECTION_RECOVERY_PROTOCOL_2026_05_29",
    "SYNTHETIC_PIPELINE_READINESS_ONLY_NOT_EMPIRICAL",
    "YtRFiniteElasticInput",
    "YtRFrozenElasticityCoefficient",
    "ytrGravitationalElasticCorrection",
    "YtRSyntheticInjection",
    "YtRSyntheticInjectionRecovered",
    "YtRSyntheticInjectionRecoveryProtocol",
    "ytr_synthetic_injection_recovered",
    "ytr_synthetic_injection_recovery_is_pipeline_readiness_only",
    "ytr_synthetic_injection_recovery_is_not_empirical_witness",
    "rfl",
]
for token in required_lean_tokens:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

if "import Chronos.Frontier.YtRSyntheticInjectionRecoveryProtocol" not in ROOT_IMPORT.read_text():
    raise SystemExit("missing root import")

doc_text = DOC.read_text()
required_doc_tokens = [
    "Status: `SYNTHETIC_PIPELINE_READINESS_ONLY_NOT_EMPIRICAL`",
    "Does not prove: empirical evidence.",
    "Does not prove: real likelihood evidence.",
    "Does not prove: independent replication.",
    "Does not prove: physical validation.",
    "Does not prove: new physics.",
    "Does not prove: new dark-matter science.",
    "Does not prove: Lambda-CDM failure evidence.",
    "Does not prove: dark matter replacement.",
    "Does not prove: predictive law closure.",
    "Does not prove: unrestricted Chronos-RR.",
    "Does not prove: unrestricted H4.1/FGL.",
    "Does not prove: P vs NP.",
    "Does not prove: any Clay problem.",
]
for token in required_doc_tokens:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

artifact = json.loads(ART.read_text())
if artifact["id"] != "YTR_SYNTHETIC_INJECTION_RECOVERY_PROTOCOL_2026_05_29":
    raise SystemExit("wrong artifact id")
if artifact["status"] != "SYNTHETIC_PIPELINE_READINESS_ONLY_NOT_EMPIRICAL":
    raise SystemExit("wrong artifact status")
if artifact["classification"] != "synthetic pipeline-readiness infrastructure":
    raise SystemExit("wrong artifact classification")

for boundary in [
    "synthetic injection-recovery only",
    "not empirical evidence",
    "not real likelihood evidence",
    "not independent replication",
    "not physical validation",
    "not new physics",
    "not new dark-matter science",
    "not Lambda-CDM failure evidence",
    "not dark matter replacement",
    "not predictive law closure",
    "not unrestricted Chronos-RR",
    "not unrestricted H4.1/FGL",
    "not P vs NP",
    "not any Clay problem",
]:
    if boundary not in artifact["boundary"]:
        raise SystemExit(f"missing boundary: {boundary}")

print("YTR_SYNTHETIC_INJECTION_RECOVERY_PROTOCOL_OK")
