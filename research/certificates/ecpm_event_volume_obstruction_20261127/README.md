# ECPM event-volume reconstruction obstruction

Status: LEAN_VERIFIED.

## Mathematical result

Four-dimensional product-order interval scaling does
not suffice to imply a Minkowski realization.

The certificate establishes a global midpoint-volume
upper bound and its exact attainment at one sixteenth
of the original interval volume.

It also establishes a concrete ordered four-event
witness whose square-root interval volumes cannot be
realized as squared Minkowski intervals in signature
(+---).

The obstruction follows from the impossibility of two
mutually orthogonal positive vectors in that signature.

## Load-bearing Lean declarations

- Chronos.ECPM.EventVolume.product_midpoint_scaling
- Chronos.ECPM.EventVolume.product_volume_not_minkowski
- Chronos.ECPM.EventVolume.no_two_orthogonal_positive

## Verification

- Mac Lean compilation: PASS
- Axiom audit: 16/16
- Unauthorized axioms: zero
- Compiler errors: zero
- Linter warnings: zero
- Certificate checksums: PASS

Reproduce from the repository root:

    lake env lean research/certificates/ecpm_event_volume_obstruction_20261127/EventVolumeObstruction.lean

## Scope

The product-order model and its algebraic interval
volume functional are specified explicitly.

This certificate refutes dimension-only reconstruction
as a sufficient criterion for Minkowski geometry.

It does not derive special or general relativity from
intrinsic event dynamics, prove physical spacetime
emergence, or disprove relativity.

Scientific novelty and independent review are not
established.

ECPM means Emergent Causal-Poset Measure.
