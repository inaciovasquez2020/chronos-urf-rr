# WEC Pointwise Positivity for Nonnegative Scalar Potential

Status: `ADMISSIBLE_LEMMA_PROVED_ALGEBRAIC_ONLY`

Corrected object name:

`WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL`

Rejected object name:

`WEC_POINTWISE_PRESERVATION_FOR_NONNEGATIVE_SCALAR_POTENTIAL`

Reason: the proved result is algebraic pointwise positivity, not dynamical preservation under Einstein-matter evolution.

## Proved Lean theorems

- `wec_pointwise_positivity_for_nonnegative_scalar_potential`
- `scalarFieldEnergyDensity_nonneg`

## Mathematical content

For real `pi`, `gradSq`, and `potentialValue`, if

```text
gradSq ≥ 0
potentialValue ≥ 0
then
(1 / 2) * pi^2 + (1 / 2) * gradSq + potentialValue ≥ 0
This proves the pointwise algebraic WEC positivity of scalar-field matter with nonnegative potential.
Open blockers not solved here
EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY
NON_SYMMETRIC_EINSTEIN_SCALAR_CONTINUATION_CRITERION
RAYCHAUDHURI_FOCUSING_WITH_SHEAR_CONTROL
NON_SYMMETRIC_TRAPPED_SURFACE_TRIGGER_FROM_CONCENTRATION
UNRESTRICTED_PHYSICS_THEOREM_ANALYTIC_CORE
Boundary
This does not prove PDE evolution.
This does not prove WEC preservation under time evolution.
This does not prove a continuation criterion.
This does not prove finite-time collapse.
This does not prove trapped-surface existence.
This does not prove unrestricted gravity closure.
This does not prove cosmic censorship.
This does not prove the hoop conjecture.
This does not prove a four-dimensional non-symmetric collapse theorem.
This does not prove any Clay problem.
