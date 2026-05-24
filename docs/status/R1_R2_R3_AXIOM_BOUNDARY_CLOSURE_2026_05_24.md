# R1/R2/R3 conditional assumption surface

Status: `CONDITIONAL_ASSUMPTION_SURFACE_ONLY_NOT_CLOSURE`.

This record replaces the failed opaque-boundary closure with a Prop-valued conditional assumption surface.

Bridge assumptions recorded as propositions:

- `R1FiniteDataToGeneralProofPromotionBridgeAssumption`
- `R2FiniteDataToGeneralProofPromotionBridgeAssumption`
- `R3FiniteDataToGeneralProofPromotionBridgeAssumption`
- `RepositoryNativeR1R2R3ToNonFactorisationBridgeAssumption`

Assumption package:

- `R1R2R3ConditionalAssumptionSurface`

Conditional Lean surfaces:

- `RepositoryNativeR1R2R3InstanceTarget_conditional_on_surface`
- `NonFactorisationProofTarget_conditional_on_surface`
- `R1R2R3PromotionProofTargetRegistry_conditional_on_surface`

Boundary:

- not theorem-level R1 closure
- not theorem-level R2 closure
- not theorem-level R3 closure
- not theorem-level NON_FACTORISATION closure
- no Chronos-RR closure
- no H4.1/FGL closure
- no P vs NP closure
- no Clay-problem closure
