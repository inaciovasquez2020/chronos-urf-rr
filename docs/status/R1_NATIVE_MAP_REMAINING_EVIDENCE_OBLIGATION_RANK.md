# R1 Native-Map Remaining Evidence Obligation Rank

Status: `R1_NATIVE_MAP_REMAINING_EVIDENCE_OBLIGATION_RANK`

Date: 2026-06-22

Input head: `e14a3781`

## Boundary

The full native-map input contract is not discharged.

The unconditional non-factorization theorem is not proved.

This document ranks the remaining evidence obligations only. It does not supply
any missing evidence.

## Ranked remaining obligations

1. `r1SourceToNativeCompatibility`

   Target interface: `R1SourceToNativeCompatibilityDischargeTarget`.

   Invariant shape: `R1SourceToNativeCompatibilityInvariantShape`.

   Invariant target: `r1_source_to_native_compatibility_invariant_shape_target`.

   Missing evidence field: `sourceToNativeCompatibilityEvidence`.

   Reason: this is the glue obligation needed to transport concrete
   Newstein/FGL source data into the native-map input contract shape. Its
   invariant shape is now named, but evidence inhabiting that invariant is still
   missing.

2. `r1DiameterSeparationFillingObstruction`

   Target interface: `R1DiameterSeparationFillingObstructionDischargeTarget`.

   Missing evidence field: `diameterSeparationFillingObstructionEvidence`.

   Reason: this is a geometric obstruction obligation and remains unproved even
   though its discharge-target interface exists.

3. `r1UniformLocalTypeCapacity`

   Target interface: `R1UniformLocalTypeCapacityDischargeTarget`.

   Missing evidence field: `uniformLocalTypeCapacityEvidence`.

   Reason: this is a capacity-bound obligation and remains unproved even though
   its discharge-target interface exists.

## Next bounded improvement

Connect the source-to-native compatibility invariant-shape target to the
source-to-native discharge-target proposition, without supplying evidence.
