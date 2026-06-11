#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "Chronos/Frontier/FinalCarrierDomainToSemanticRankRateCertificate.lean"
doc = ROOT / "docs/status/CHRONOS_FINAL_CARRIER_DOMAIN_TO_SEMANTIC_RANK_RATE_CERTIFICATE_2026_05_13.md"
artifact = ROOT / "artifacts/chronos/final_carrier_domain_to_semantic_rank_rate_certificate_2026_05_13.json"
root = ROOT / "Chronos.lean"

for p in [lean, doc, artifact, root]:
    if not p.exists():
        print(f"missing {p.relative_to(ROOT)}", file=sys.stderr)
        sys.exit(1)

lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "theorem FinalCarrierDomain_repository_native_semantic_rank_rate_exhaustiveness",
    "RepositoryNativeSemanticRankRateExhaustiveness",
    "theorem FinalCarrierDomain_to_RepositoryNativeSemanticRankRateDomain",
    "theorem FinalCarrierDomain_to_native_SemanticRankRateCertificate_exists",
    "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n",
    "exact FinalCarrierDomain_repository_native_semantic_rank_rate_exhaustiveness c hc",
]

required_doc = [
    "CONDITIONAL_IMPORTER_ONLY",
    "RepositoryNativeSemanticRankRateExhaustiveness",
    "FinalCarrierDomain_to_native_SemanticRankRateCertificate_exists",
    "This is a conditional importer surface only.",
    "It does not prove:",
    "UniversalFiberEntropyGap",
    "P_ne_NP",
]

for token in required_lean:
    if token not in lean_text:
        print(f"missing Lean token: {token}", file=sys.stderr)
        sys.exit(1)

for token in required_doc:
    if token not in doc_text:
        print(f"missing doc token: {token}", file=sys.stderr)
        sys.exit(1)

if "import Chronos.Frontier.FinalCarrierDomainToSemanticRankRateCertificate" not in root_text:
    print("missing Chronos.lean import", file=sys.stderr)
    sys.exit(1)

if data.get("status") != "CONDITIONAL_IMPORTER_ONLY":
    print("bad status", file=sys.stderr)
    sys.exit(1)

if data.get("theorem_level_closure") is not False:
    print("bad theorem_level_closure", file=sys.stderr)
    sys.exit(1)

for forbidden in [
    "theorem FinalCarrierDomain_to_SemanticRankRateCertificate :",
    "SemanticRankRateCertificate c := by",
    "UniversalFiberEntropyGap proved",
    "Chronos-RR closed",
    "H4.1/FGL closed",
    "P vs NP proved",
    "Clay problem solved",
]:
    if forbidden in lean_text or forbidden in doc_text or forbidden in json.dumps(data):
        print(f"forbidden token present: {forbidden}", file=sys.stderr)
        sys.exit(1)

print("FinalCarrierDomain repository-native SemanticRankRateCertificate conditional surface verified.")
