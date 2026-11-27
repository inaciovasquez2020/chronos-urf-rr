# Chronos-ECPM persistent event certificates

Status: scoped mathematical research.
Mac Lean verification: PASS, 16 declarations.
Independent CI reproduction: pending.

## Persistent algebra certificate

Eight declarations establish mixture-density identities,
positive covariance identities and algebraic curvature witnesses.

The curvature witness verifies positivity of the stated
expression, not its differential-geometric derivation.

## Population certificate

Eight declarations establish nonnegative binary observation
masses, normalization at arbitrary finite lengths, extension
consistency and nonindependence of a two-component mixture.

The first population compilation failed because real-number
division required noncomputable definitions. The repair changed
only the computability annotations of mix and total.
The repaired source and successful receipt are preserved.

## Scope restrictions

These certificates do not formalize the full continuous
quantum-event measure, Haar distribution, causal-poset
embedding, differential-geometric curvature derivation,
Einstein field equations or a fundamental physical law.

Physical selection of the collective state, identification
of event density with physical volume, empirical validation
and independent mathematical novelty remain OPEN.

## Verification

Lean 4.29.0
Mathlib 69cbc416b3f58ba11e331db067644d0508e78341

Original Mac HEAD:
a999b816df08bc393036cc7ebe8d0a6ed1939b6b

Each certificate includes its original source, compiler
receipt, dependency manifest, toolchain and checksums.

From each certificate directory:

    shasum -a 256 -c SHA256SUMS

Recompile each source using the recorded dependency
environment and audit all sixteen declarations against
the standard Lean axiom allowlist.

No repository-wide verification is claimed.
