# Derived Finite Registered Hyperbolic Natural Admissibility Certificate — 2026-05-27

Status: `DERIVED_FINITE_REGISTERED_HYPERBOLIC_CERTIFICATE_CLOSED_ONE_STACK_TARGET_ONLY`

This strengthens the previous finite registered hyperbolic certificate by deriving the computable target's `objectCount`, `semanticRankRate`, and `fiberEntropyGap` from the finite registry arity rather than hand-setting those fields directly in the target.

## Derived target data

```lean
def derivedFiniteRegisteredHyperbolicObjectCount
def derivedFiniteRegisteredHyperbolicSemanticRankRate
def derivedFiniteRegisteredHyperbolicFiberEntropyGap
Closed dominance
theorem derivedFiniteRegisteredHyperbolicRankEntropyDominance
Closed certificate
def derivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate :
    NaturalAdmissibilityDominanceCertificate
      derivedFiniteRegisteredHyperbolicComputableTargetApplication
Closed consequence
theorem derivedFiniteRegisteredHyperbolicTargetYieldsNaturalDominance :
    Nonempty NaturalDominanceAdmissibleComputableClass
Next missing ingredient
Replace registry-arity equality dominance with an application-derived nontrivial rank-to-gap inequality.
Boundary
Does not prove:
certificate construction for every concrete target application
certificate construction for arbitrary finite registered hyperbolic registries
nontrivial rank-to-gap inequality
raw opaque admissibility implies dominance
RawToStructuredAdmissibilityDominance for the old raw class
stability under admissible limits
finite-support approximation theorem
unrestricted semantic-rank-to-fiber-entropy bridge
UniversalFiberEntropyGap
Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
