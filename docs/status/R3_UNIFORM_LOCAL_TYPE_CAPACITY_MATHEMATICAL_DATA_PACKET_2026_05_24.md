# R3 Uniform Local-Type Capacity Mathematical Data Packet

Status: `R3_DATA_PACKET_COMPUTABLE_NO_PROOF_CLAIM`

This adds the third concrete mathematical-data packet for the R1/R2/R3 route.

The checker computes radius-`r` local type signatures from finite labeled graph data and rejects the packet if the number of distinct local types exceeds the supplied capacity bound.

## Supplied finite data

- vertices: `u0, u1, u2, u3, u4, u5`
- graph: 6-cycle
- labels: alternating `A/B`
- radius: `1`
- capacity bound: `2`
- distinct local types: `A|B,B`, `B|A,A`
- distinct local-type count: `2`
- computed capacity instance: present

## Boundary

Does not prove:

- general UniformLocalTypeCapacity
- native R1/R2/R3 instance
- LongChordExclusion
- DiameterSeparationFillingObstruction
- NON_FACTORISATION
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
