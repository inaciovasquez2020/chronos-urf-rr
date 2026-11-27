# ECPM constructive Lorentzian reconstruction

Status: LEAN_VERIFIED — CONDITIONAL.

This standalone certificate preserves the previous
16-declaration event-volume obstruction and adds nine
audited reconstruction declarations.

## Results

- Explicit Lorentzian embedding from relational feature data.
- Preservation of reconstructed signed intervals.
- Injectivity and chronological agreement under stated hypotheses.
- Constructive triangular factorization from scalar pivot conditions.
- Removal of the supplied Minkowski frame hypothesis.

## Load-bearing declarations

- positive_lorentzian_reconstruction
- exists_triangular_frame
- positive_reconstruction_from_pivots

## Verification

Mac Lean compilation: PASS.
Axiom audit: 25/25.
Unauthorized axioms: zero.
Compiler errors: zero.
Linter warnings: zero.

Reproduce from the repository root:

    lake env lean research/certificates/ecpm_positive_reconstruction_20261127/EventVolumeObstruction.lean

## Scope and limitations

The reconstruction assumes scalar pivot positivity,
injective relational features, chronological consistency,
and agreement with prescribed comparable-pair measurements.

The certificate constructs a Lorentzian frame under those
conditions. It does not derive the conditions from an
intrinsic event-generation law.

General anchor inversion and anchor-feature consistency,
global uniqueness, continuum volume preservation, physical
spacetime emergence, and Einstein gravitational dynamics
are not established by this Lean certificate.

Scientific novelty and independent review remain unestablished.

Predecessor: Chronos PR #1389.
