# R2 Diameter/Separation/Filling Mathematical Data Packet

Status: `R2_DATA_PACKET_COMPUTABLE_NO_PROOF_CLAIM`

This adds the second concrete mathematical-data packet for the R1/R2/R3 route.

The checker computes graph diameter and terminal-pair distances by BFS, validates filling certificates, and rejects the packet if the finite obstruction condition is absent.

## Supplied finite data

- vertices: `a, b, c, d, e, f`
- graph: path graph `a-b-c-d-e-f`
- terminal pairs: `a--d`, `b--e`, `c--f`
- diameter bound: `5`
- separation threshold: `3`
- filling floor: `2`
- graph diameter: `5`
- minimum terminal separation: `3`
- minimum filling size: `3`
- computed obstruction: present

## Boundary

Does not prove:

- general DiameterSeparationFillingObstruction
- native R1/R2/R3 instance
- LongChordExclusion
- UniformLocalTypeCapacity
- NON_FACTORISATION
- Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
