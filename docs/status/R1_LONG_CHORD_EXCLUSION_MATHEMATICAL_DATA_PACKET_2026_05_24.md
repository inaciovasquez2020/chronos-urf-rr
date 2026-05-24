# R1 Long-Chord Exclusion Mathematical Data Packet

Status: `R1_DATA_PACKET_COMPUTABLE_NO_PROOF_CLAIM`

This adds the first concrete mathematical-data packet for the R1 route.

The checker computes finite skeleton distances by BFS and rejects the packet if any supplied candidate chord has skeleton distance greater than or equal to the long-chord threshold.

## Supplied finite data

- vertices: `v0, v1, v2, v3, v4`
- skeleton edges: path graph `v0-v1-v2-v3-v4`
- candidate chords: `v0--v2`, `v1--v3`, `v2--v4`
- threshold: `3`
- maximum candidate skeleton distance: `2`
- computed long chords: none

## Boundary

Does not prove:

- general LongChordExclusion
- native R1/R2/R3 instance
- DiameterSeparationFillingObstruction
- UniformLocalTypeCapacity
- NON_FACTORISATION
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
