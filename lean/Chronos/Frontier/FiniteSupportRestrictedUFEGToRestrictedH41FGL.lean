import Chronos.Frontier.RestrictedChronosRRToRestrictedH41FGL

namespace Chronos
namespace Frontier

/--
Finite-support restricted UFEG data feeding the already restricted
Chronos-RR-to-H4.1/FGL bridge.
-/
structure FiniteSupportRestrictedUFEGToRestrictedH41FGLData where
  Carrier : Type
  finiteSupport : Prop
  admissibleRestrictedDomain : Prop
  restrictedUFEG : Prop

def toRestrictedChronosRRData
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    RestrictedChronosRRData where
  Carrier := D.Carrier
  finiteSupport := D.finiteSupport
  admissibleRestrictedDomain := D.admissibleRestrictedDomain
  restrictedUFEG := D.restrictedUFEG

/--
Finite-support restricted UFEG over the admissible restricted domain.
-/
abbrev FiniteSupportRestrictedUFEG
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) : Prop :=
  D.finiteSupport ∧ D.admissibleRestrictedDomain ∧ D.restrictedUFEG

/--
Restricted H4.1/FGL target obtained over the induced restricted Chronos-RR data.
-/
abbrev FiniteSupportRestrictedH41FGL
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) : Prop :=
  RestrictedH41FGL (toRestrictedChronosRRData D)

theorem finite_support_restricted_ufeg_to_restricted_chronos_rr
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData)
    (h : FiniteSupportRestrictedUFEG D) :
    RestrictedChronosRR (toRestrictedChronosRRData D) := by
  exact h

theorem finite_support_restricted_ufeg_to_restricted_h41_fgl
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData)
    (h : FiniteSupportRestrictedUFEG D) :
    FiniteSupportRestrictedH41FGL D := by
  exact RestrictedChronosRRToRestrictedH41FGL
    (toRestrictedChronosRRData D)
    (finite_support_restricted_ufeg_to_restricted_chronos_rr D h)

theorem FiniteSupportRestrictedUFEGToRestrictedH41FGL
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D → FiniteSupportRestrictedH41FGL D := by
  intro h
  exact finite_support_restricted_ufeg_to_restricted_h41_fgl D h

end Frontier
end Chronos
