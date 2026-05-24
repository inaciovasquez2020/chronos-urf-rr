# R1/R2/R3 Non-Factorisation Promotion Lock

Status: `CONDITIONAL_INTERFACE_AND_NO_PROMOTION_LOCK_ONLY`.

This packet formalizes the R1, R2, and R3 substep interfaces:

- R1a, R1b, R1c.
- R2a, R2b, R2c, R2d.
- R3a, R3b, R3c, R3d.

It also adds the conditional dependency-chain surface:

`R1_R2_R3_TO_NON_FACTORISATION`.

Promotion rule:

Chronos-RR and H4.1/FGL promotion are blocked unless all three theorem-level inputs are supplied:

- `R1_theorem_proved`
- `R2_theorem_proved`
- `R3_theorem_proved`

Boundary:

- does not prove LongChordExclusion
- does not prove DiameterSeparationFillingObstruction
- does not prove UniformLocalTypeCapacity
- does not prove NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
