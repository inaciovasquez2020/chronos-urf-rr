# Restricted Stationary Gravity Estimate Candidate — 2026-05-28

Status: `RESTRICTED_CANDIDATE_LEMMA_ONLY_NO_GRAVITY_ESTIMATE_PROOF`

## Candidate lemma

For static-or-axisymmetric asymptotically flat Einstein-matter data with rotationally symmetric quasi-local surface `S` of area-radius `r > 2M`, test the restricted estimate

    QL_gate(data; S) <= C(r, M) * (int_Sigma mu_0 dV + O(r^-3)) + Flux_infty^(0)(r)

where `E_grav(data)` is instantiated by ADM/Bondi mass plus matter-density control, and `Flux_boundary(data; S)` is instantiated by a Komar-type or Hawking quasi-local boundary term subject to positivity/sign and decay hypotheses.

## Missing restricted lemmas

1. `RestrictedStationarySurfaceAdmissibility`
2. `RestrictedKomarHawkingFluxSign`
3. `RestrictedAsymptoticDecayErrorBound`
4. `RestrictedQLGateMassControl`

## Shape test

Failure of this restricted candidate under stationary symmetry, sign, and decay hypotheses flags the unrestricted `ConcreteGravityCoerciveEstimate` shape as malformed or incorrectly oriented.

## Boundary

This artifact is a restricted candidate lemma only.

It does not prove the restricted estimate, the coercive estimate, an analytic estimate, an Einstein-matter theorem, a collapse theorem, Cosmic Censorship, the Hoop Conjecture, quantum gravity, unrestricted Chronos-RR, unrestricted H4.1/FGL, P vs NP, or any Clay problem.
