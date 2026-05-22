# Filled Explicit Stress-Energy Evolution Identity Calculation

Status: `FORMULA_PAYLOAD_FILLED_CONDITIONAL_NO_EVOLUTION_THEOREM`

## Object

`FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION`

## Depends on

- `WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL`
- `EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET`

## Fixed conventions

- Signature: `(-,+,+,+)`
- Future timelike unit normal: `n^a n_a = -1`
- Spatial projection: `gamma_ab = g_ab + n_a n_b`
- Scalar normal derivative: `Pi = n^a nabla_a phi`
- Spatial derivative: `D_i phi = gamma_i^a nabla_a phi`

## Filled formulas

```text
T_ab = nabla_a phi nabla_b phi
       - (1/2) g_ab (nabla^c phi nabla_c phi)
       - g_ab V(phi)
rho = (1/2) Pi^2 + (1/2) |D phi|_gamma^2 + V(phi)
j_i = - Pi D_i phi
S_ij = D_i phi D_j phi
       + (1/2) gamma_ij (Pi^2 - |D phi|_gamma^2)
       - gamma_ij V(phi)
S = (3/2) Pi^2 - (1/2) |D phi|_gamma^2 - 3 V(phi)
Candidate normal-projected energy identity
Conditional on the scalar Euler-Lagrange equation
Box_g phi - V'(phi) = 0
the stress-energy tensor satisfies
nabla_a T^{ab} = 0
The candidate normal-projected target is recorded as
n^a nabla_a rho =
  -D_i j^i + K_ij S^ij + K rho - 2 a_i j^i
with
a_i = D_i log N
Coordinate target shape
For
partial_t = N n + beta
the target shape is
(partial_t - Lie_beta) rho =
  N[-D_i j^i + K_ij S^ij + K rho - 2 a_i j^i]
Remaining blockers
SIGN_CONVENTION_CHECK_NOT_DISCHARGED
GAUGE_TERM_CHECK_NOT_DISCHARGED
BOUNDARY_FLUX_CONTROL_NOT_PROVED
CANDIDATE_IDENTITY_NOT_LEAN_FORMALIZED
NO_WEC_PRESERVATION_THEOREM
NO_CONTINUATION_CRITERION
Next admissible object
GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY
Boundary
This is a formula-payload object only.
It does not prove an unconditional stress-energy evolution identity.
It does not prove WEC preservation under time evolution.
It does not prove a continuation criterion.
It does not prove Raychaudhuri focusing with shear control.
It does not prove trapped-surface existence.
It does not prove finite-time collapse.
It does not prove unrestricted gravity closure.
It does not prove cosmic censorship.
It does not prove the hoop conjecture.
It does not prove a four-dimensional non-symmetric collapse theorem.
It does not prove any Clay problem.
