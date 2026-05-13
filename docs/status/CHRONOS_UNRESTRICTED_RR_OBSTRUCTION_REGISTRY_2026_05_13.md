# Chronos unrestricted RR obstruction registry

Status: UNRESTRICTED_CHRONOS_RR_OBSTRUCTION_REGISTRY_LOCKED

Lean artifact:

- `Chronos/Frontier/UnrestrictedChronosRRObstructionRegistry.lean`

Registry:

- `unrestrictedChronosRRObstructionRegistry`

Main theorem:

- `repository_native_conditional_closure_has_remaining_unrestricted_obstruction`

Canonical witness:

- `canonical_repository_native_conditional_closure_has_remaining_unrestricted_obstruction`

Dependency:

- `repository_native_chronos_rr_conditional_closure_from_depth_bridge`

Registered obstructions:

- `missingUnrestrictedDepthBridge`
- `missingUnrestrictedUniversalFiberEntropyGap`
- `missingSemanticRankRateToFiberEntropySoundness`
- `repositoryNativeOnly`

Boundary:

- Locks the obstruction registry separating repository-native conditional Chronos-RR from unrestricted Chronos-RR.
- Does not prove unrestricted Chronos-RR closure.
- Does not prove unrestricted DepthBridge.
- Does not prove unrestricted UniversalFiberEntropyGap.
- Does not prove SemanticRankRateToFiberEntropySoundness.
- Does not prove H4.1/FGL closure.
- Does not prove P vs NP closure.
- Does not prove any Clay-problem closure.
