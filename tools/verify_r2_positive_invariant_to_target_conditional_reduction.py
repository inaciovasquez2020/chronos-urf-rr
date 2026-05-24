#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "lean/Chronos/Frontier/R2PositiveInvariantToTargetConditionalReduction.lean"
artifact = ROOT / "artifacts/chronos/r2_positive_invariant_to_target_conditional_reduction_2026_05_24.json"
status = ROOT / "docs/status/R2_POSITIVE_INVARIANT_TO_TARGET_CONDITIONAL_REDUCTION_2026_05_24.md"

lean_text = lean.read_text()
status_text = status.read_text()
data = json.loads(artifact.read_text())

for token in [
    "import Chronos.Frontier.R2AdmissibilityGatedPositiveInvariant",
    "structure R2FinalObstructionTransferLemma",
    "def R2FinalObstructionTransferLemmaSupplied",
    "structure R2PositiveInvariantToTargetConditionalReduction",
    "def R2PositiveInvariantToTargetReduction",
    "theorem r2_positive_invariant_ready_for_conditional_reduction",
    "theorem r2_positive_invariant_to_target_conditional_reduction",
    "def r2FinalObstructionTransferLemmaStatus",
    "theorem r2_conditional_reduction_closed_count",
    "theorem no_r2_theorem_target_closed_by_conditional_reduction",
]:
    assert token in lean_text, token

assert data["status"] == "R2_CONDITIONAL_REDUCTION_CLOSED_FINAL_TRANSFER_LEMMA_OPEN"
assert data["terminal_missing_lemma"] == "R2FinalObstructionTransferLemma"
assert data["conditional_reduction_closed_count"] == 1
assert data["r2_theorem_target_closure_count"] == 0
assert len(data["closed_theorems"]) == 4

for token in [
    "R2FinalObstructionTransferLemma",
    "DiameterSeparationFillingObstructionProofTarget",
    "R2 theorem target closure",
    "R3 theorem target closure",
    "NON_FACTORISATION theorem target closure",
    "FourBridgesSourceSolved theorem closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in status_text, token
    assert token in data["still_open"] or token in data["does_not_prove"], token

print("r2 positive invariant to target conditional reduction verifier OK")
