import Chronos.Frontier.FiniteSupportRestrictedTerminalH41FGLLock

namespace Chronos
namespace Frontier

/--
Boundary lock produced by the finite-support restricted terminal H4.1/FGL surface.
This is a restricted-domain boundary lock only; it does not promote any
unrestricted H4.1/FGL, P vs NP, or Clay statement.
-/
structure FiniteSupportRestrictedBoundaryLock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) : Prop where
  terminal_h41fgl :
    FiniteSupportRestrictedTerminalH41FGLLock D
  restricted_domain_only :
    FiniteSupportRestrictedUFEG D

theorem finite_support_restricted_boundary_lock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData)
    (h : FiniteSupportRestrictedUFEG D) :
    FiniteSupportRestrictedBoundaryLock D := by
  exact
    { terminal_h41fgl :=
        FiniteSupportRestrictedTerminalH41FGLLock_from_UFEG D h
      restricted_domain_only := h }

theorem FiniteSupportRestrictedBoundaryLock_from_UFEG
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D →
      FiniteSupportRestrictedBoundaryLock D := by
  intro h
  exact finite_support_restricted_boundary_lock D h

end Frontier
end Chronos
