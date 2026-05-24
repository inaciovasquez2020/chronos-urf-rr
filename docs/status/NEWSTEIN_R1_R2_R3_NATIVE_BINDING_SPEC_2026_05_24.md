# Newstein R1/R2/R3 Native Binding Spec

Status: `SPECIFICATION_ONLY_NO_NATIVE_INSTANCE`.

This packet adds the Lean object:

`RepositoryNativeR1R2R3BindingSpec`

It records the exact repository-native data required before R1/R2/R3 can be treated as theorem-proved in the Newstein non-factorisation route.

Required native data:

- `nativeR1Data : R1SemanticData`
- `nativeR2Data : R2SemanticData`
- `nativeR3Data : R3SemanticData`

Required correctness fields:

- `r1Correct : R1LongChordExclusionTheorem nativeR1Data`
- `r2Correct : R2DiameterSeparationFillingObstructionTheorem nativeR2Data`
- `r3Correct : R3UniformLocalTypeCapacityTheorem nativeR3Data`

Required registry-matching fields:

- `nativeWTrivSpec`
- `nativePhi2TrivSpec`
- `nativeBoundaryOperatorSpec`
- `nativeSupportSpec`
- `nativeLongChordSpec`
- `nativeFiberClassSpec`
- `nativeFiberToGlobalQuotientSpec`
- `nativeTwoChainSpec`
- `nativeDiameterSpec`
- `nativeSeparationParameterSpec`
- `nativeQuotientDataSpec`
- `nativeLocalTypeSpec`
- `nativeCapacityFunctionSpec`
- `r1MatchesOpenInputsRegistry`
- `r2MatchesOpenInputsRegistry`
- `r3MatchesOpenInputsRegistry`

Closed surfaces:

- `repository_native_R1_R2_R3_theorems_from_binding_spec`
- `repository_native_nonfactorisation_promotion_from_binding_spec`
- `no_repository_native_promotion_without_binding_supplied`
- `no_repository_native_chronos_rr_promotion_without_binding_supplied`
- `no_repository_native_h41_fgl_promotion_without_binding_supplied`

Boundary:

- specification only
- does not construct RepositoryNativeR1R2R3BindingSpec
- does not prove LongChordExclusion
- does not prove DiameterSeparationFillingObstruction
- does not prove UniformLocalTypeCapacity
- does not prove NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
