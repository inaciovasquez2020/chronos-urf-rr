import Chronos.Frontier.NaturalAdmissibilityToDominanceClass

namespace Chronos.Frontier

/--
First target certificate frontier.

This isolates the weakest remaining target-local object after
`NaturalAdmissibilityToDominanceClass`: for a concrete target class `X`,
one must construct a `NaturalAdmissibilityDominanceCertificate X`.

This module intentionally does not construct such a certificate.
-/
structure FirstTargetNaturalAdmissibilityCertificateFrontier
    (X : ComputableFiniteAdmissibleClass) : Prop where
  certificate :
    NaturalAdmissibilityDominanceCertificate X

theorem firstTargetNaturalAdmissibilityCertificateFrontier_to_natural
    {X : ComputableFiniteAdmissibleClass}
    (h : FirstTargetNaturalAdmissibilityCertificateFrontier X) :
    Nonempty (NaturalDominanceAdmissibleComputableClass) := by
  exact ⟨{
    base := X
    natural_certificate := h.certificate
  }⟩

end Chronos.Frontier
