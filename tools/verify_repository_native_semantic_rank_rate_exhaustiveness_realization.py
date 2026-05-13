#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/RepositoryNativeSemanticRankRateExhaustivenessRealization.lean"
doc = root / "docs/status/CHRONOS_REPOSITORY_NATIVE_SEMANTIC_RANK_RATE_EXHAUSTIVENESS_REALIZATION_2026_05_13.md"
artifact = root / "artifacts/chronos/repository_native_semantic_rank_rate_exhaustiveness_realization_2026_05_13.json"
chrono = root / "Chronos.lean"

required = {
    lean: [
        "import Chronos.Frontier.RepositoryNativeSemanticRankRateExhaustiveness",
        "def RepositoryNativeSemanticRankRateWitnessObligation : Prop",
        "∀ c : ChronosCarrierData",
        "FinalCarrierDomain c",
        "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n",
        "theorem repository_native_semantic_rank_rate_witness_obligation_equiv_exhaustiveness",
        "theorem repository_native_semantic_rank_rate_exhaustiveness_realization_from_exhaustiveness",
        "RepositoryNativeSemanticRankRateExhaustiveness →",
        "RepositoryNativeSemanticRankRateExhaustivenessRealization",
        "FRONTIER_OPEN / WITNESS_REALIZATION_ONLY",
    ],
    doc: [
        "Status: `FRONTIER_OPEN / WITNESS_REALIZATION_ONLY`",
        "`RepositoryNativeSemanticRankRateExhaustivenessRealization`",
        "∀ c : ChronosCarrierData",
        "FinalCarrierDomain c",
        "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n",
        "RepositoryNativeSemanticRankRateExhaustiveness",
        "RepositoryNativeSemanticRankRateExhaustivenessRealization",
        "No unrestricted UniversalFiberEntropyGap theorem.",
        "No Chronos-RR.",
        "No H4.1/FGL.",
        "No P vs NP.",
        "No Clay closure.",
    ],
    chrono: [
        "import Chronos.Frontier.RepositoryNativeSemanticRankRateExhaustivenessRealization",
    ],
}

for path, needles in required.items():
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

    text = path.read_text()

    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{path} missing required text: {needle}")

if not artifact.exists():
    raise SystemExit(f"missing required file: {artifact}")

data = json.loads(artifact.read_text())

if data.get("status") != "FRONTIER_OPEN / WITNESS_REALIZATION_ONLY":
    raise SystemExit("artifact status mismatch")

if data.get("weakest_missing_object") != "RepositoryNativeSemanticRankRateExhaustivenessRealization":
    raise SystemExit("weakest missing object mismatch")

if data.get("theorem_level_closure") is not False:
    raise SystemExit("artifact must preserve theorem_level_closure=false")

required_boundary = {
    "No unrestricted UniversalFiberEntropyGap theorem",
    "No Chronos-RR",
    "No H4.1/FGL",
    "No P vs NP",
    "No Clay closure",
}

if set(data.get("boundary", [])) != required_boundary:
    raise SystemExit("boundary mismatch")

forbidden = [
    "Chronos-RR closed",
    "H4.1/FGL closed",
    "P vs NP solved",
    "Clay closure achieved",
    "unrestricted UniversalFiberEntropyGap theorem proved",
    "UniversalFiberEntropyGap theorem proved",
]

combined = "\n".join(path.read_text() for path in [lean, doc, artifact])

for token in forbidden:
    if token in combined:
        raise SystemExit(f"forbidden overclaim token present: {token}")

print("RepositoryNativeSemanticRankRateExhaustivenessRealization frontier verified.")
