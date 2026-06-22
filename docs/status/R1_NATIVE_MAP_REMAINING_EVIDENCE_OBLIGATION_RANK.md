# R1 Native-Map Remaining Evidence Obligation Rank

Status: `R1_NATIVE_MAP_REMAINING_EVIDENCE_OBLIGATION_RANK`

Date: 2026-06-22

Input head: `a1b631db`

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

   Evidence shape: `R1SourceToNativeCompatibilityEvidenceShape`.

   Conditional discharge bridge:
   `r1_source_to_native_compatibility_discharge_target_from_evidence_shape`.

   Target projection:
   `r1_source_to_native_compatibility_from_evidence_shape_target_eq`.

   Missing evidence field: `sourceToNativeCompatibilityEvidence`.

   Reason: this is the glue obligation needed to transport concrete
   Newstein/FGL source data into the native-map input contract shape. Its
   invariant shape and conditional evidence-shape-to-discharge-target bridge are
   now named, but an inhabitant of the compatibility evidence shape is still
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

Introduce a missing-inhabitant boundary lock for
`R1SourceToNativeCompatibilityEvidenceShape`, without constructing an
inhabitant.
