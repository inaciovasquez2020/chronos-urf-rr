# R1 Native-Map Input Contract Decomposition Status

Status: `R1_NATIVE_MAP_INPUT_CONTRACT_DECOMPOSITION_STATUS`

Date: 2026-06-22

Input head: `a60847f6`

## What is closed

The R1 long-chord field now has a positive wired path:

- concrete Newstein/FGL source object;
- concrete R1 long-chord discharge target;
- extraction of the long-chord component from the native-map input contract.

This is a field-level contract decomposition only.

## What is still missing

The full native-map input contract is not discharged.

The remaining missing evidence fields are:

1. `r1SourceToNativeCompatibility`, now represented by `R1SourceToNativeCompatibilityDischargeTarget` but still without evidence;
2. `r1DiameterSeparationFillingObstruction`, now represented by `R1DiameterSeparationFillingObstructionDischargeTarget` but still without evidence;
3. `r1UniformLocalTypeCapacity`, now represented by `R1UniformLocalTypeCapacityDischargeTarget` but still without evidence.

Each missing evidence field remains blocked from full native-map input-contract discharge.

## Ranked weakest points

1. Source-to-native compatibility evidence for the existing discharge target interface.
2. Diameter-separation filling-obstruction evidence for the existing discharge target interface.
3. Uniform local-type capacity evidence for the existing discharge target interface.
4. Full native-map input-contract constructor.

## Boundary

No full native-map input contract is proved.

No unconditional non-factorization theorem is proved.

This rollup is a status artifact only. It does not add new theorem evidence.
