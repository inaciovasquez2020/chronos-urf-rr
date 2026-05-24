# Native long-chord / diameter / capacity ingredients

Status: `STRUCTURAL_INGREDIENT_PACKET_CLOSED_PROMOTION_FRONTIER_OPEN`.

## Closed in this packet

- Defined exact native objects appearing in the long-chord layer:
  - `LongChordEndpoint`
  - `LongChordMetricDatum`
  - `LongChordNativeObject`
  - `LongChordWitness`
  - `NativeLongChordCoherence`
- Proved one contradiction lemma:
  - `long_chord_witness_contradiction`
- Defined the diameter/filling compatibility invariant:
  - `DiameterFillingNativeObject`
  - `DiameterFillingCompatibility`
- Proved one monotone separation lower bound:
  - `monotone_separation_lower_bound`
- Defined explicit local-type capacity bound:
  - `ExplicitLocalTypeCapacityC = 4096`
  - `WithinExplicitLocalTypeCapacity`
  - `local_type_capacity_bound_certificate`

## Still open

- `R1PromotionProofObstructionEliminationCertificate`
- `R2PromotionProofObstructionEliminationCertificate`
- `R3PromotionProofObstructionEliminationCertificate`
- `NonFactorisationBridgeProofObstructionEliminationCertificate`

## Boundary

Does not prove:
- `R1PromotionProofTarget`
- `R2PromotionProofTarget`
- `R3PromotionProofTarget`
- `NonFactorisationBridgeProofTarget`
- LongChordExclusion
- DiameterSeparationFillingObstruction
- UniformLocalTypeCapacity
- native R1/R2/R3 instance unconditionally
- NON_FACTORISATION unconditionally
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
