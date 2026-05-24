# R1/R2/R3 Progressive Witness Packet

Status: `PROGRESSIVE_TEST_HARNESS_ONLY_FRONTIER_OPEN`

This adds a fillable test harness for the R1/R2/R3 route.

The packet is intentionally staged:

1. `R1_LONG_CHORD_EXCLUSION_DATA`
2. `R1_LONG_CHORD_EXCLUSION_VERIFIER`
3. `R1_LONG_CHORD_EXCLUSION_LEAN_PROOF`
4. `R2_DIAMETER_SEPARATION_FILLING_DATA`
5. `R2_DIAMETER_SEPARATION_FILLING_VERIFIER`
6. `R2_DIAMETER_SEPARATION_FILLING_LEAN_PROOF`
7. `R3_UNIFORM_LOCAL_TYPE_CAPACITY_DATA`
8. `R3_UNIFORM_LOCAL_TYPE_CAPACITY_VERIFIER`
9. `R3_UNIFORM_LOCAL_TYPE_CAPACITY_LEAN_PROOF`
10. `REPOSITORY_NATIVE_R1_R2_R3_INSTANCE`
11. `REPOSITORY_NATIVE_R1_R2_R3_BINDING_CLOSURE`

Default verification accepts the open frontier packet.

Strict verification fails until all R1/R2/R3/CLOSURE targets are filled with repository-native proof artifacts.

## Boundary

Does not prove:

- native R1/R2/R3 instance
- LongChordExclusion
- DiameterSeparationFillingObstruction
- UniformLocalTypeCapacity
- NON_FACTORISATION
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
