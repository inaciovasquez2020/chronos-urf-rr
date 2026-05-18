import Mathlib

namespace Chronos
namespace Frontier

/--
Restricted carrier domain data for the finite-support restricted Chronos-RR route.
This file is intentionally restricted: all implications remain internal to the
selected/admissible finite-support domain.
-/
structure RestrictedChronosRRData where
  Carrier : Type
  admissible : Carrier → Prop
  finiteSupport : Prop
  positiveSupportFloor : Prop
  restrictedUFEG : Prop

/--
Restricted Chronos-RR is recorded only as a domain-indexed target over the
finite-support/admissible carrier surface.
-/
structure RestrictedChronosRR (D : RestrictedChronosRRData) : Prop where
  finite_support : D.finiteSupport
  positive_floor : D.positiveSupportFloor
  gap : D.restrictedUFEG

/--
Restricted H4.1/FGL is the next restricted target reached from restricted
Chronos-RR, still confined to the same admissible finite-support domain.
-/
structure RestrictedH41FGL (D : RestrictedChronosRRData) : Prop where
  finite_support : D.finiteSupport
  positive_floor : D.positiveSupportFloor
  transferred_gap : D.restrictedUFEG

theorem restricted_h41_fgl_from_restricted_chronos_rr
    (D : RestrictedChronosRRData)
    (h : RestrictedChronosRR D) :
    RestrictedH41FGL D := by
  exact
    { finite_support := h.finite_support
      positive_floor := h.positive_floor
      transferred_gap := h.gap }

theorem RestrictedChronosRRToRestrictedH41FGL
    (D : RestrictedChronosRRData) :
    RestrictedChronosRR D → RestrictedH41FGL D := by
  intro h
  exact restricted_h41_fgl_from_restricted_chronos_rr D h

end Frontier
end Chronos
