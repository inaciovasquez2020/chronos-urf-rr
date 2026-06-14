#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "lean/Chronos/Frontier/RestrictedConcentrationControlsContinuationNormLemma.lean"
text = lean.read_text()

required_tokens = [
    "RestrictedConcentrationControlsContinuationNormLemmaData",
    "RestrictedConcentrationControlsContinuationNormLemmaHypotheses",
    "RestrictedConcentrationControlsContinuationNormLemmaObligation",
    "RestrictedConcentrationControlsContinuationNormLemmaSurface",
    "RestrictedConcentrationControlsContinuationNormLemmaStatus",
    "RestrictedConcentrationControlsContinuationNormLemmaFlagshipObject",
    "RestrictedConcentrationControlsContinuationNormLemmaName",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "RESTRICTED_CONCENTRATION_CONTROLS_CONTINUATION_NORM_LEMMA",
    "LEMMA_SURFACE_ONLY_NO_ANALYTIC_CONTINUATION_NORM_CONTROL_PROOF",
    "NO_UNCONDITIONAL_RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM",
    "does not prove unconditional restricted continuation norm control",
]

for token in required_tokens:
    assert token in text, token

for forbidden in ["axiom ", "opaque ", "sorry", "admit"]:
    assert forbidden not in text, forbidden

print("RESTRICTED_CONCENTRATION_CONTROLS_CONTINUATION_NORM_LEMMA_SURFACE_OK")
print("Status: LEMMA_SURFACE_ONLY_NO_ANALYTIC_CONTINUATION_NORM_CONTROL_PROOF")
print("Flagship object: RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF")
