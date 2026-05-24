# R1/R2/R3 Finite Data Promotion Assumptions

Status: `PROMOTION_ASSUMPTION_LAYER_ONLY_NON_FACTORISATION_CONDITIONAL`

This adds an explicit promotion-assumption layer on top of the finite-data Lean certificates.

## Added assumptions

- `R1FiniteDataToGeneralProofPromotionAssumption`
- `R2FiniteDataToGeneralProofPromotionAssumption`
- `R3FiniteDataToGeneralProofPromotionAssumption`

## Conditional assembly

- `repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions`

## NON_FACTORISATION status

NON_FACTORISATION remains conditional via:

- `NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance`
- `non_factorisation_from_finite_data_promotion_assumptions_conditional`
- `r1_r2_r3_promotion_assumptions_to_non_factorisation_conditional_surface`

## Remaining open objects

- proof of `R1FiniteDataToGeneralProofPromotionAssumption`
- proof of `R2FiniteDataToGeneralProofPromotionAssumption`
- proof of `R3FiniteDataToGeneralProofPromotionAssumption`
- proof of `NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance`

## Boundary

Does not prove:

- LongChordExclusion
- DiameterSeparationFillingObstruction
- UniformLocalTypeCapacity
- native R1/R2/R3 instance unconditionally
- NON_FACTORISATION unconditionally
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
