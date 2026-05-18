# Unconditional UniversalFiberEntropyGap Obstruction — 2026-05-18

Status: `UNCONDITIONAL_UFEG_OBSTRUCTED`.

## Closed

This formalizes the obstruction to an unconditional universal fiber entropy
gap over arbitrary fiber-mass data.

Closed Lean targets:

- `FiberMassUniformFloor`
- `zeroFiberMassData_no_uniform_floor`
- `no_uniform_floor_of_arbitrarily_small`
- `unconditional_universal_fiber_entropy_gap_obstructed`

## Mathematical content

Arbitrary fiber-mass data does not imply a uniform positive lower bound.

A zero-mass package has no positive uniform floor. More generally, any package
with arbitrarily small fiber masses has no uniform positive floor.

Therefore an unrestricted `UniversalFiberEntropyGap` theorem over arbitrary
fiber-mass data requires an additional positivity/coercivity assumption or a
restricted domain.

## Boundary

This proves only the obstruction.

Does not prove:

- restricted `UniversalFiberEntropyGap`
- admissible-domain H4.1/FGL beyond the existing selected-domain chain
- unrestricted Chronos-RR
- P vs NP
- any Clay problem
