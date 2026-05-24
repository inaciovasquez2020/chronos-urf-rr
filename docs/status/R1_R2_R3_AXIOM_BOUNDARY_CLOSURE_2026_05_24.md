# R1/R2/R3 opaque-boundary declaration

Status: `OPAQUE_ASSUMPTION_DECLARATION_ONLY`.

This record makes the four missing R1/R2/R3 bridge assumptions explicit as opaque declarations.

Declared opaque assumptions:

- `r1_finite_data_to_general_proof_promotion_assumption`
- `r2_finite_data_to_general_proof_promotion_assumption`
- `r3_finite_data_to_general_proof_promotion_assumption`
- `repository_native_r1_r2_r3_instance_to_non_factorisation_assumption`

Opaque-dependent Lean surfaces:

- `RepositoryNativeR1R2R3InstanceTarget_derived_under_opaque_boundary`
- `NonFactorisationProofTarget_derived_under_opaque_boundary`
- `R1R2R3PromotionProofTargetRegistry_derived_under_opaque_boundary`

Boundary:

- not theorem-level R1 closure
- not theorem-level R2 closure
- not theorem-level R3 closure
- not theorem-level NON_FACTORISATION closure
- no Chronos-RR closure
- no H4.1/FGL closure
- no P vs NP closure
- no Clay-problem closure
