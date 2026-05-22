# Gauge Sign and Boundary Check for Explicit Stress-Energy Evolution Identity

Status: `GAUGE_SIGN_BOUNDARY_CHECK_RECORDED_CONDITIONAL_NO_IDENTITY_PROMOTION`

## Object

`GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY`

## Depends on

- `WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL`
- `EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET`
- `FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION`

## Fixed conventions

```text
signature = (-,+,+,+)
n^a n_a = -1
gamma_ab = g_ab + n_a n_b
partial_t = N n + beta
Pi = n^a nabla_a phi
D_i phi = gamma_i^a nabla_a phi
The extrinsic-curvature sign remains locked:
K_ij convention must be checked against K_ij = -1/2 Lie_n gamma_ij before theorem promotion.
Candidate identity under selected conventions
n^a nabla_a rho =
  -D_i j^i + K_ij S^ij + K rho - 2 a_i j^i
(partial_t - Lie_beta) rho =
  N[-D_i j^i + K_ij S^ij + K rho - 2 a_i j^i]
a_i = D_i log N
Gauge checks
The lapse acceleration term is retained.
The shift contribution is retained through Lie_beta rho.
No gauge term is discarded.
No harmonic-gauge simplification is assumed.
No boundary gauge normalization is assumed.
Boundary-flux checks
The divergence term -D_i j^i is retained.
Boundary contribution over partial Omega is not assumed to vanish.
Asymptotically flat flux vanishing is not assumed.
Compact-without-boundary cancellation is not assumed.
Periodic-boundary cancellation is not assumed.
Remaining blockers
EXTRINSIC_CURVATURE_SIGN_CONVENTION_NOT_EXTERNALLY_DISCHARGED
BOUNDARY_FLUX_VANISHING_NOT_PROVED
CANDIDATE_IDENTITY_NOT_LEAN_FORMALIZED_AS_TENSOR_THEOREM
NO_WEC_PRESERVATION_THEOREM
NO_CONTINUATION_CRITERION
NO_COLLAPSE_TRIGGER_DERIVATION
Next admissible object
LEAN_FORMAL_STRESS_ENERGY_IDENTITY_OR_EXTERNAL_TENSOR_AUDIT
Boundary
This is a gauge-sign and boundary-check surface only.
It does not prove an unconditional stress-energy evolution identity.
It does not prove WEC preservation under time evolution.
It does not prove an energy estimate.
It does not prove a continuation criterion.
It does not prove Raychaudhuri focusing with shear control.
It does not prove trapped-surface existence.
It does not prove finite-time collapse.
It does not prove unrestricted gravity closure.
It does not prove cosmic censorship.
It does not prove the hoop conjecture.
It does not prove a four-dimensional non-symmetric collapse theorem.
It does not prove any Clay problem.
