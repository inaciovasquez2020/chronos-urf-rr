import Mathlib

namespace Chronos
namespace Frontier

/--
Restricted carrier domain data for the finite-support restricted Chronos-RR route.
This surface is intentionally restricted to the admissible finite-support domain.
-/
structure RestrictedChronosRRData where
  Carrier : Type
  finiteSupport : Prop
  admissibleRestrictedDomain : Prop
  restrictedUFEG : Prop

/--
Restricted Chronos-RR over the finite-support admissible domain.
-/
abbrev RestrictedChronosRR (D : RestrictedChronosRRData) : Prop :=
  D.finiteSupport ∧ D.admissibleRestrictedDomain ∧ D.restrictedUFEG

/--
Restricted H4.1/FGL over the same finite-support admissible domain.
-/
abbrev RestrictedH41FGL (D : RestrictedChronosRRData) : Prop :=
  D.finiteSupport ∧ D.admissibleRestrictedDomain ∧ D.restrictedUFEG

theorem restricted_h41_fgl_from_restricted_chronos_rr
    (D : RestrictedChronosRRData)
    (h : RestrictedChronosRR D) :
    RestrictedH41FGL D := by
  exact h

theorem restricted_chronos_rr_to_restricted_h41_fgl
    (D : RestrictedChronosRRData) :
    RestrictedChronosRR D → RestrictedH41FGL D := by
  intro h
  exact restricted_h41_fgl_from_restricted_chronos_rr D h

theorem RestrictedChronosRRToRestrictedH41FGL
    (D : RestrictedChronosRRData) :
    RestrictedChronosRR D → RestrictedH41FGL D := by
  exact restricted_chronos_rr_to_restricted_h41_fgl D

end Frontier
end Chronos
