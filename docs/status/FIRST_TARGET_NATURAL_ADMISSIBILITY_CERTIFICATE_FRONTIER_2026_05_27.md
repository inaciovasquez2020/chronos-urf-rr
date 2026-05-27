# First Target Natural Admissibility Certificate Frontier — 2026-05-27

Status: `FIRST_TARGET_CERTIFICATE_FRONTIER_ONLY`

This records the first target-local certificate frontier after
`NaturalAdmissibilityToDominanceClass`.

## Frontier object

```lean
structure FirstTargetNaturalAdmissibilityCertificateFrontier
    (X : ComputableFiniteAdmissibleClass) : Prop where
  certificate :
    NaturalAdmissibilityDominanceCertificate X
Closed implication
theorem firstTargetNaturalAdmissibilityCertificateFrontier_to_dominance
    {X : ComputableFiniteAdmissibleClass}
    (h : FirstTargetNaturalAdmissibilityCertificateFrontier X) :
    Nonempty (DominanceAdmissibleComputableClass)
Next missing ingredient
Construct NaturalAdmissibilityDominanceCertificate X for a named concrete target application.
Boundary
Does not prove:
certificate construction for any concrete target application
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
