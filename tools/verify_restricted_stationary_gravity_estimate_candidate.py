#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/restricted_stationary_gravity_estimate_candidate_2026_05_28.json"
DOC = ROOT / "docs/status/RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/RestrictedStationaryGravityEstimateCandidate.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

assert data["id"] == "RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_V1"
assert data["status"] == "RESTRICTED_CANDIDATE_LEMMA_ONLY_NO_GRAVITY_ESTIMATE_PROOF"
assert data["candidate_estimate"] == "QL_gate(data; S) <= C(r, M) * (int_Sigma mu_0 dV + O(r^-3)) + Flux_infty^(0)(r)"

for token in [
    "static-or-axisymmetric",
    "r > 2M",
]:
    assert token in data["restricted_regime"], token

for item in [
    "RestrictedStationarySurfaceAdmissibility",
    "RestrictedKomarHawkingFluxSign",
    "RestrictedAsymptoticDecayErrorBound",
    "RestrictedQLGateMassControl",
]:
    assert item in data["missing_lemmas"], item

for token in [
    "restricted candidate lemma only",
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
    data["candidate_estimate"],
    "RestrictedKomarHawkingFluxSign",
    "RestrictedAsymptoticDecayErrorBound",
    "malformed or incorrectly oriented",
    "does not prove the restricted estimate",
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
    "structure RestrictedStationaryGravityEstimateCandidate",
    "restrictedStationaryGravityEstimateCandidateV1",
    "restrictedStationaryGravityEstimateCandidateV1_status",
    "restrictedStationaryGravityEstimateCandidateV1_candidate",
    "restrictedStationaryGravityEstimateCandidateV1_boundary",
]:
    assert token in lean, token

assert "import Chronos.Frontier.RestrictedStationaryGravityEstimateCandidate" in ROOT_LEAN.read_text()

print("RESTRICTED_STATIONARY_GRAVITY_ESTIMATE_CANDIDATE_OK")
