#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "Chronos/Frontier/RepositoryNativeSemanticRankRateFromGlobalCertificate.lean"
artifact = ROOT / "artifacts/chronos/repository_native_semantic_rank_rate_from_global_certificate_2026_05_13.json"
doc = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_SEMANTIC_RANK_RATE_FROM_GLOBAL_CERTIFICATE_2026_05_13.md"
root = ROOT / "Chronos.lean"

for p in [lean, artifact, doc, root]:
    if not p.exists():
        print(f"missing {p.relative_to(ROOT)}", file=sys.stderr)
        sys.exit(1)

lean_text = lean.read_text()
doc_text = doc.read_text()
root_text = root.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "theorem RepositoryNativeSemanticRankRateExhaustiveness_from_global_certificate",
    "(h : ∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n)",
    "RepositoryNativeSemanticRankRateExhaustiveness := by",
    "intro c hc",
    "exact h",
]

required_doc = [
    "CONDITIONAL_REDUCTION_ONLY",
    "native_semantic_rank_rate_certificate_exists",
    "This is a conditional reduction only.",
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

if "import Chronos.Frontier.RepositoryNativeSemanticRankRateFromGlobalCertificate" not in root_text:
    print("missing Chronos.lean import", file=sys.stderr)
    sys.exit(1)

if data.get("status") != "CONDITIONAL_REDUCTION_ONLY":
    print("bad status", file=sys.stderr)
    sys.exit(1)

if data.get("theorem_level_closure") is not False:
    print("bad theorem_level_closure", file=sys.stderr)
    sys.exit(1)

if data.get("minimal_missing_object") != "native_semantic_rank_rate_certificate_exists":
    print("bad minimal_missing_object", file=sys.stderr)
    sys.exit(1)

for forbidden in [
    "axiom ",
    "admit",
    "sorry",
    "native_semantic_rank_rate_certificate_exists :=",
    "UniversalFiberEntropyGap proved",
    "Chronos-RR closed",
    "H4.1/FGL closed",
    "P vs NP proved",
    "Clay problem solved",
]:
    if forbidden in lean_text or forbidden in doc_text or forbidden in json.dumps(data):
        print(f"forbidden token present: {forbidden}", file=sys.stderr)
        sys.exit(1)

print("RepositoryNativeSemanticRankRateExhaustiveness global-certificate reduction verified.")
