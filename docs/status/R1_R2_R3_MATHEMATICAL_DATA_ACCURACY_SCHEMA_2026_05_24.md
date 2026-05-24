# R1/R2/R3 Mathematical Data Accuracy Schema

Status: `MATHEMATICAL_DATA_SCHEMA_ONLY_NO_ACCURACY_CLAIM`

This adds the required mathematical-data layer for the progressive R1/R2/R3 harness.

The schema blocks premature accuracy claims. It only permits a structural completeness score after each target supplies:

- formal statement
- domain
- objects
- invariants
- obstruction or capacity quantity
- finite witness schema
- proof dependencies
- checker contract
- Lean target
- boundary

Accuracy policy:

- score type: `STRUCTURAL_COMPLETENESS_ONLY`
- no truth accuracy claim
- no empirical accuracy claim
- no theorem accuracy claim

Does not prove:

- mathematical accuracy
- truth accuracy
- native R1/R2/R3 instance
- LongChordExclusion
- DiameterSeparationFillingObstruction
- UniformLocalTypeCapacity
- NON_FACTORISATION
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
