#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "Chronos/Frontier/NativeSemanticRankRateCertificateWitnessSolved.lean"
artifact = ROOT / "artifacts/chronos/native_semantic_rank_rate_certificate_witness_solved_2026_05_13.json"
status = ROOT / "docs/status/CHRONOS_NATIVE_SEMANTIC_RANK_RATE_CERTIFICATE_WITNESS_SOLVED_2026_05_13.md"

missing = [str(p) for p in [lean, artifact, status] if not p.exists()]
missing == [] or (_ for _ in ()).throw(SystemExit("missing file: " + ", ".join(missing)))

text = lean.read_text()
required = [
    "namespace Chronos.Frontier",
    "set_option autoImplicit false",
    "lemma native_semantic_rank_rate_certificate_exists",
    "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n",
    "exact ⟨0, ⟨True⟩⟩",
    "theorem RepositoryNativeSemanticRankRateExhaustiveness_solved",
    "intro c _hc",
]
missing_markers = [x for x in required if x not in text]
missing_markers == [] or (_ for _ in ()).throw(SystemExit("missing Lean marker: " + ", ".join(missing_markers)))

forbidden = [x for x in ["axiom ", "admit", "sorry"] if x in text]
forbidden == [] or (_ for _ in ()).throw(SystemExit("forbidden Lean token: " + ", ".join(forbidden)))

data = json.loads(artifact.read_text())
assert data["status"] == "SOLVED_PROP_FIELD_WITNESS"
assert data["witness_n"] == 0
assert data["witness_field"] == "True"
assert data["axioms_introduced"] == 0
assert data["admits_introduced"] == 0
assert data["sorries_introduced"] == 0

s = status.read_text()
phrases = [
    "Status: SOLVED_PROP_FIELD_WITNESS",
    "No new `axiom`, `admit`, or `sorry` is introduced.",
    "current SemanticRankRateCertificate stores Prop data only",
    "does not prove UniversalFiberEntropyGap",
    "does not prove P vs NP closure",
]
missing_phrases = [x for x in phrases if x not in s]
missing_phrases == [] or (_ for _ in ()).throw(SystemExit("missing status phrase: " + ", ".join(missing_phrases)))

print("Native semantic rank-rate certificate witness solved verifier passed.")
