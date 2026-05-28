#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/restricted_komar_hawking_flux_sign_target_2026_05_28.json"
DOC = ROOT / "docs/status/RESTRICTED_KOMAR_HAWKING_FLUX_SIGN_TARGET_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/RestrictedKomarHawkingFluxSignTarget.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

assert data["id"] == "RESTRICTED_KOMAR_HAWKING_FLUX_SIGN_TARGET_V1"
assert data["status"] == "RESTRICTED_FLUX_SIGN_TARGET_ONLY_NO_SIGN_PROOF"
assert data["parent_candidate"] == "RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_V1"
assert data["target_lemma"] == "RestrictedKomarHawkingFluxSign"
assert "Flux_boundary(data; S) >= 0" in data["sign_claim_shape"]

for item in [
    "orientation convention for S",
    "energy condition used for sign",
    "normalization of Komar/Hawking quantity",
    "asymptotic decay hypothesis",
    "surface admissibility hypothesis",
]:
    assert item in data["missing_inputs"], item

for token in [
    "target lemma only",
    "no flux sign proof",
    "no restricted estimate proof",
    "no coercive estimate proof",
    "no analytic estimate proof",
    "no Einstein-matter theorem",
    "no collapse theorem",
    "no Cosmic Censorship",
    "no Hoop Conjecture",
    "no quantum gravity",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]:
    assert token in data["boundary"], token

doc = DOC.read_text()
for token in [
    data["status"],
    data["parent_candidate"],
    data["target_lemma"],
    "Flux_boundary(data; S) >= 0",
    "does not prove the flux sign",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in doc, token

lean = LEAN.read_text()
for token in [
    "structure RestrictedKomarHawkingFluxSignTarget",
    "restrictedKomarHawkingFluxSignTargetV1",
    "restrictedKomarHawkingFluxSignTargetV1_status",
    "restrictedKomarHawkingFluxSignTargetV1_lemma",
    "restrictedKomarHawkingFluxSignTargetV1_boundary",
]:
    assert token in lean, token

assert "import Chronos.Frontier.RestrictedKomarHawkingFluxSignTarget" in ROOT_LEAN.read_text()

print("RESTRICTED_KOMAR_HAWKING_FLUX_SIGN_TARGET_OK")
