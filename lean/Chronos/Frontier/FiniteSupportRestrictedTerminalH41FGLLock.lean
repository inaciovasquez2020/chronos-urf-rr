import Chronos.Frontier.FiniteSupportRestrictedEndToEndLock

namespace Chronos
namespace Frontier

/--
Terminal restricted H4.1/FGL lock for the finite-support admissible route.
This packages the already closed finite-support restricted end-to-end theorem
as a terminal restricted surface only.
-/
structure FiniteSupportRestrictedTerminalH41FGLLock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) : Prop where
  restricted_h41_fgl : FiniteSupportRestrictedH41FGL D

theorem finite_support_restricted_terminal_h41fgl_lock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData)
    (h : FiniteSupportRestrictedUFEG D) :
    FiniteSupportRestrictedTerminalH41FGLLock D := by
  exact
    { restricted_h41_fgl :=
        FiniteSupportRestrictedEndToEndH41FGL D h }

theorem FiniteSupportRestrictedTerminalH41FGLLock_from_UFEG
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D →
      FiniteSupportRestrictedTerminalH41FGLLock D := by
  intro h
  exact finite_support_restricted_terminal_h41fgl_lock D h

end Frontier
end Chronos
