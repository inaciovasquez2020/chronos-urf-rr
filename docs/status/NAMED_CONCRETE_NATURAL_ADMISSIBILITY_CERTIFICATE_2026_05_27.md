# Named Concrete Natural Admissibility Certificate — 2026-05-27

Status: `NAMED_CONCRETE_CERTIFICATE_CLOSED_ONE_TARGET_ONLY`

This closes the first named concrete instance of the natural-admissibility certificate interface.

## Named target

```lean
def firstNamedConcreteTargetApplication :
    ComputableFiniteAdmissibleClass
Closed certificate
def firstNamedConcreteNaturalAdmissibilityCertificate :
    NaturalAdmissibilityDominanceCertificate
      firstNamedConcreteTargetApplication
Frontier instance
def firstNamedConcreteCertificateFrontier :
    FirstTargetNaturalAdmissibilityCertificateFrontier
      firstNamedConcreteTargetApplication
Closed consequence
theorem firstNamedConcreteTargetYieldsNaturalDominance :
    Nonempty NaturalDominanceAdmissibleComputableClass
Next missing ingredient
Construct NaturalAdmissibilityDominanceCertificate X for a non-toy target application already used by the Chronos-RR bridge stack.
Boundary
Does not prove:
certificate construction for every concrete target application
certificate construction for any non-toy target application
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
