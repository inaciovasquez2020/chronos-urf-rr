#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/concrete_gravity_coercive_estimate_proof_obligation_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_GRAVITY_COERCIVE_ESTIMATE_PROOF_OBLIGATION_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteGravityCoerciveEstimateProofObligation.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

assert data["id"] == "CONCRETE_GRAVITY_COERCIVE_ESTIMATE_PROOF_OBLIGATION_V1"
assert data["status"] == "PROOF_OBLIGATION_ONLY_NO_COERCIVE_ESTIMATE_PROOF"
assert data["curvature_energy_norm"] == "E_grav(data)"
assert data["quasi_local_collapse_functional"] == "QL_gate(data; S)"
assert data["boundary_flux_error"] == "Flux_boundary(data; S)"
assert data["estimate_shape"] == "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)"

for token in [
    "proof obligation only",
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
    data["id"],
    "E_grav(data)",
    "QL_gate(data; S)",
    "Flux_boundary(data; S)",
    "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)",
    "does not prove the coercive estimate",
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
    "structure ConcreteGravityCoerciveEstimateProofObligation",
    "concreteGravityCoerciveEstimateProofObligationV1",
    "concreteGravityCoerciveEstimateProofObligationV1_status",
    "concreteGravityCoerciveEstimateProofObligationV1_shape",
    "concreteGravityCoerciveEstimateProofObligationV1_boundary",
]:
    assert token in lean, token

assert "import Chronos.Frontier.ConcreteGravityCoerciveEstimateProofObligation" in ROOT_LEAN.read_text()

print("CONCRETE_GRAVITY_COERCIVE_ESTIMATE_PROOF_OBLIGATION_OK")
