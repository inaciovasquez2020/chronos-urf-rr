# FourBridgesSourceSolved OPEN Target

Status: `FOUR_BRIDGES_SOURCE_SOLVED_OPEN_TARGET_ONLY`.

This packet adds the OPEN target `FourBridgesSourceSolved`.

It records one theorem stub per bridge:

- `solve_R1_bridge_theorem_stub`
- `solve_R2_bridge_theorem_stub`
- `solve_R3_bridge_theorem_stub`
- `solve_NON_FACTORISATION_bridge_theorem_stub`

It records one counterexample-search harness per bridge:

- `r1_counterexample_search_harness`
- `r2_counterexample_search_harness`
- `r3_counterexample_search_harness`
- `non_factorisation_counterexample_search_harness`

Exactly one bridge route is acted on first:

- `unrestricted_r1_native_promotion_refuted_first`

This refutes only the unrestricted native R1 promotion route using a native-admissible long-chord counterexample.

Does not prove:

- `RepositoryNativeR1LongChordCoherence`
- `NoRepositoryNativeLongChordWitness`
- `LongChordExclusionProofTarget`
- `DiameterSeparationFillingObstructionProofTarget`
- `UniformLocalTypeCapacityProofTarget`
- `NonFactorisationBridgeProofTarget`
- `NON_FACTORISATION`
- `Chronos-RR`
- `H4.1/FGL`
- `P vs NP`
- any Clay problem
