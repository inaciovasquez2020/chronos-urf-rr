# R1/R2/R3 promotion obstruction frontier lock

Status: `PROMOTION_OBSTRUCTION_FRONTIER_LOCKED_OPEN`.

This records that all four obstruction-certificate surfaces are present:

- `R1PromotionProofObstructionCertificate`
- `R2PromotionProofObstructionCertificate`
- `R3PromotionProofObstructionCertificate`
- `NonFactorisationBridgeProofObstructionCertificate`

## Closure requires

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
