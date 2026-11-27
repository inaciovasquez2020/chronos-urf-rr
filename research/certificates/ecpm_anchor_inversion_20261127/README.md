# ECPM anchor inversion

Status: LEAN_VERIFIED — CONDITIONAL.

Extends Chronos PR #1390 with six audited declarations.

The certificate establishes anchor-feature identities,
radial measurement recovery, uniqueness of inverse
coefficients, and conditional Lorentzian reconstruction.

Validation:
- Lean compilation: PASS
- Audited declarations: 31
- New declarations: 6
- Unauthorized axioms: zero

Reproduce from the repository root:

    lake env lean research/certificates/ecpm_anchor_inversion_20261127/AnchorInversion.lean

Explicit inverse, consistency and Lorentzian pivot
hypotheses remain required.

This certificate does not establish intrinsic event
generation, physical volume selection, global continuum
uniqueness, emergent gravity or Einstein field equations.

Scientific novelty and independent review remain
unestablished.
